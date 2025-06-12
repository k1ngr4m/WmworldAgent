import logging
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import CsMatchDetail

# 获取日志记录器
logger = logging.getLogger('csgo_stats')


def index(request):
    """主页视图"""
    logger.info("访问主页")
    return render(request, 'index.html')


def search_player(request):
    """搜索玩家视图"""
    query = request.GET.get('query', '')
    logger.info(f"搜索玩家: {query}")

    if not query:
        return render(request, 'search_results.html', {'error': '请输入玩家名称或SteamID'})

    # 根据玩家名称或SteamID搜索
    try:
        # 先尝试将查询转换为数字，看是否是SteamID
        playerId = int(query)
        matches = CsMatchDetail.objects.filter(playerId=playerId).order_by('-startTime')
    except ValueError:
        # 如果不是数字，则认为是玩家名称
        matches = CsMatchDetail.objects.filter(nickName__icontains=query).order_by('-startTime')

    # 获取唯一的玩家信息
    players = {}
    for match in matches:
        if match.playerId not in players:
            players[match.playerId] = {
                'player_id': match.playerId,
                'nick_name': match.nickName,
                'matches_count': 1,
                'last_match': match.startTime
            }
        else:
            players[match.playerId]['matches_count'] += 1
            if match.startTime > players[match.playerId]['last_match']:
                players[match.playerId]['last_match'] = match.startTime

    player_list = list(players.values())
    player_list.sort(key=lambda x: x['last_match'], reverse=True)

    logger.info(f"找到 {len(player_list)} 个玩家")
    return render(request, 'search_results.html', {
        'query': query,
        'players': player_list,
        'matches_count': len(matches)
    })


def player_detail(request, player_id):
    """玩家详情页视图"""
    logger.info(f"查看玩家详情: {player_id}")

    # 获取玩家信息
    matches = CsMatchDetail.objects.filter(playerId=player_id).order_by('-startTime')
    if not matches:
        return render(request, 'player_detail.html', {'error': '未找到该玩家的比赛记录'})

    # 计算玩家统计数据
    player = matches[0]  # 使用第一个匹配的记录获取玩家基本信息

    # 计算总比赛数
    total_matches = matches.count()

    # 计算总击杀、死亡和助攻
    total_kills = sum(m.kills for m in matches)
    total_deaths = sum(m.deaths for m in matches)
    total_assists = sum(m.assists for m in matches)

    # 计算平均数据
    avg_kills = total_kills / total_matches if total_matches > 0 else 0
    avg_deaths = total_deaths / total_matches if total_matches > 0 else 0
    avg_assists = total_assists / total_matches if total_matches > 0 else 0
    avg_rating = sum(m.rating for m in matches) / total_matches if total_matches > 0 else 0

    # 计算胜率
    win_matches = matches.filter(win=True).count()
    win_rate = (win_matches / total_matches) * 100 if total_matches > 0 else 0

    # 按地图统计
    map_stats = {}
    for match in matches:
        if match.mapEn not in map_stats:
            map_stats[match.mapEn] = {'count': 0, 'wins': 0, 'kills': 0, 'deaths': 0}

        map_stats[match.mapEn]['count'] += 1
        if match.win:
            map_stats[match.mapEn]['wins'] += 1
        map_stats[match.mapEn]['kills'] += match.kills
        map_stats[match.mapEn]['deaths'] += match.deaths

    # 计算每个地图的胜率和K/D
    for map_name, stats in map_stats.items():
        stats['win_rate'] = (stats['wins'] / stats['count']) * 100 if stats['count'] > 0 else 0
        stats['kd'] = stats['kills'] / stats['deaths'] if stats['deaths'] > 0 else float('inf')

    # 排序地图统计
    sorted_map_stats = sorted(map_stats.items(), key=lambda x: x[1]['count'], reverse=True)

    logger.info(f"玩家 {player.nickName} 共有 {total_matches} 场比赛记录")
    return render(request, 'player_detail.html', {
        'player': player,
        'matches': matches[:10],  # 只显示最近10场比赛
        'total_matches': total_matches,
        'avg_kills': round(avg_kills, 2),
        'avg_deaths': round(avg_deaths, 2),
        'avg_assists': round(avg_assists, 2),
        'avg_rating': round(avg_rating, 2),
        'win_rate': round(win_rate, 2),
        'map_stats': sorted_map_stats,
        'total_kills': total_kills,
        'total_deaths': total_deaths,
        'total_assists': total_assists,
    })


def match_detail(request, match_id):
    """比赛详情页视图（重构后支持一场比赛10条玩家记录）"""
    logger.info(f"查看比赛详情: {match_id}")

    # 获取该比赛的所有玩家记录（最多10条）
    player_records = get_list_or_404(CsMatchDetail, matchId=match_id)

    if not player_records:
        return render(request, 'match_detail.html', {'error': '未找到该比赛记录'})

    # 提取比赛的共同信息（所有玩家记录的比赛信息应一致）
    match = player_records[0]  # 使用第一条记录的比赛信息

    # 按队伍分组
    team1_players = [p for p in player_records if p.teamId == match.team1PvpId]
    team2_players = [p for p in player_records if p.teamId == match.team2PvpId]

    # 计算队伍数据
    team1_score = team1_players[0].score1 if team1_players else 0
    team2_score = team1_players[0].score2 if team1_players else 0
    team1_kills = sum(p.kills for p in team1_players)
    team2_kills = sum(p.kills for p in team2_players)

    # 找出MVP（rating最高的玩家）
    all_players = team1_players + team2_players
    mvp_player = max(all_players, key=lambda p: p.rating) if all_players else None

    logger.info(f"比赛 {match_id} 共有 {len(all_players)} 名玩家")
    return render(request, 'match_detail.html', {
        'match': match,
        'all_players': all_players,
        'team1_players': team1_players,
        'team2_players': team2_players,
        'team1_score': team1_score,
        'team2_score': team2_score,
        'team1_kills': team1_kills,
        'team2_kills': team2_kills,
        'mvp_player': mvp_player,
    })