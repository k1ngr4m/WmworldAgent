import pytz

from datetime import datetime
from utils.log_util import logger


# 保留特定的键值对
def get_filtered_data(data, toSteamId):
    steam_id_str = str(toSteamId)
    win_team = data['base']['winTeam']

    def filter_participant(players, winTeam):
        return {
            "playerId": players['playerId'],
            "nickName": players['nickName'],
            "team": players['team'],
            "kills": players['kill'],            # 击杀
            "deaths": players['death'],          # 死亡
            "assists": players['assist'],        # 助攻
            "headShot": players['headShot'],            # 爆头数
            "headShotCount": players['headShotCount'],      # 爆头数
            "headShotRatio": players['headShotRatio'],  # 爆头率
            "rating": players['rating'],        # rating
            "pwRating": players['pwRating'],    # pwRating
            "flash": players['flash'],
            "flashTeammate": players['flashTeammate'],      # 闪白队友次数
            "flashSuccess": players['flashSuccess'],        # 闪白对手次数
            "mvpValue": players['mvpValue'],
            "twoKill": players['twoKill'],
            "threeKill": players['threeKill'],
            "fourKill": players['fourKill'],
            "fiveKill": players['fiveKill'],
            "vs1": players['vs1'],
            "vs2": players['vs2'],
            "vs3": players['vs3'],
            "vs4": players['vs4'],
            "vs5": players['vs5'],
            "dmgArmor": players['dmgArmor'],    # 甲伤
            "dmgHealth": players['dmgHealth'],  # 血伤
            "adpr": players['adpr'],        # ADR
            "fireCount": players['fireCount'],
            "hitCount": players['hitCount'],
            "rws": players['rws'],          # RWS
            "pvpTeam": players['pvpTeam'],
            "ranks": players['rank'],
            "we": players['we'],                    # WE
            "throwsCnt": players['throwsCnt'],      # 投掷数
            "teamId": players['teamId'],            # 队伍
            "snipeNum": players['snipeNum'],        # 狙杀
            "entryKill": players['entryKill'],      # 首杀
            "firstDeath": players['firstDeath'],    # 首死
            "mvp": players['mvp'],
            "kda": cal_kda(int(players["kill"]), int(players["death"]), int(players["assist"])),
            "kast": players['kast'],
            "handGunKill": players['handGunKill'],
            "awpKill": players['awpKill'],
            "entryDeath": players['entryDeath'],
            "botKill": players['botKill'],
            "negKill": players['negKill'],
            "damage": players['damage'],
            "multiKills": players['multiKills'],
            "itemThrow": players['itemThrow'],
            "smokeThrows": players['smokeThrows'],
            "grenadeDamage": players['grenadeDamage'],
            "infernoDamage": players['infernoDamage'],
            "score": players['score'],
            "endGame": players['endGame'],
            "userForbidDTO": players.get('userForbidDTO', ''),
            "win": cal_win(players['team'], winTeam),
            # "challenges": calculate_participant_scores(players, data),
        }

    filtered_players = [
        filter_participant(players, win_team)
        for players in data["players"]
        if players["playerId"] == steam_id_str and players is not None
    ]

    filtered_data = {
        "matchId": data['base']['matchId'],
        "map": data['base']['map'],
        "mapEn": data['base']['mapEn'],
        "startTime": dateString_to_datetime(data['base']['startTime']),
        "endTime": dateString_to_datetime(data['base']['endTime']),
        "duration": data['base']['duration'],
        "winTeam": data['base']['winTeam'],
        "score1": data['base']['score1'],
        "score2": data['base']['score2'],
        "team1PvpId": data['base']['team1PvpId'],
        "team2PvpId": data['base']['team2PvpId'],
        "pvpLadder": data['base']['pvpLadder'],
        "mode": data['base']['mode'],
        "dayOfWeek": get_chinese_day_of_week(data['base']["startTime"]),
        "players": filtered_players,
    }
    logger.debug(filtered_data)

    return filtered_data


def dateString_to_datetime(date_string):
    date_format = "%Y-%m-%d %H:%M:%S"
    traditional_format = datetime.strptime(date_string, date_format)
    return traditional_format


def get_chinese_day_of_week(date_string):
    # 映射英文星期几到中文的字典
    translation = {
        'Monday': '星期一',
        'Tuesday': '星期二',
        'Wednesday': '星期三',
        'Thursday': '星期四',
        'Friday': '星期五',
        'Saturday': '星期六',
        'Sunday': '星期日'
    }

    date_format = "%Y-%m-%d %H:%M:%S"
    dt_beijing = datetime.strptime(date_string, date_format)

    # 将日期时间转换为英文星期几
    english_day_of_week = dt_beijing.strftime('%A')

    # 返回对应的中文星期几，如果在字典中找不到对应的值，则返回原始的英文星期几
    return translation.get(english_day_of_week, english_day_of_week)


def cal_kda(kill, death, assists):
    if death == 0:
        return round((kill + assists) / (death + 1), 2)
    else:
        return round((kill + assists) / death, 2)

def cal_win(team, win_team):
    if team == win_team:
        return 1
    else:
        return 0

