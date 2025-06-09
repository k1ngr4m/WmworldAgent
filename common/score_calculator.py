import pytz

from config.championName_zh import championName_zh
from datetime import datetime
from utils.logutil import logger
from config.itemList import item_name


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
        "mapUrl": data['base']['mapUrl'],
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


def calculate_participant_scores(participant, data):
    # 从participant和data中提取所需的属性
    game_duration = round(int(data["gameDuration"]) / 60, 2)

    kda = cal_kda(int(participant["kills"]), int(participant["deaths"]), int(participant["assists"]))

    total_damage = cal_total(int(participant["physicalDamageDealtToChampions"]),
                             int(participant["magicDamageDealtToChampions"]),
                             int(participant["physicalDamageDealtToChampions"]))
    damage_per_minute = cal_per_minute(total_damage, game_duration)

    total_damage_taken = cal_total(
        int(participant["physicalDamageTaken"]),
        int(participant["magicDamageTaken"]),
        int(participant["trueDamageTaken"]))
    damage_taken_per_minute = cal_per_minute(total_damage_taken, game_duration)

    gold_earned = participant["goldEarned"]
    gold_per_minute = cal_per_minute(gold_earned, game_duration)

    damage_conversion_rate = round(total_damage / gold_earned, 4)

    # 返回计算后的属性值
    return {
        "damageConversionRate": damage_conversion_rate,  # 伤害转化率
        "damagePerMinute": damage_per_minute,
        "damageTakenPerMinute": damage_taken_per_minute,  # 分均承受伤害
        "goldPerMinute": gold_per_minute,  # 分均经济
        "kda": kda,  # kda
    }


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


def cal_per_minute(totalValue, totalTime):
    return round(totalValue / totalTime, 2)


def cal_total(physicalDamageTaken, magicDamageTaken, trueDamageTaken):
    return physicalDamageTaken + magicDamageTaken + trueDamageTaken


def cal_win(team, win_team):
    if team == win_team:
        return 1
    else:
        return 0


def replace_itemName(item_num):
    return item_name[str(item_num)]['name']
