from datetime import datetime
from utils.log_util import logger

PLAYER_FIELD_MAP = {
    "playerId": "playerId",
    "nickName": "nickName",
    "team": "team",
    "kills": "kill",
    "deaths": "death",
    "assists": "assist",
    "headShot": "headShot",
    "headShotCount": "headShotCount",
    "headShotRatio": "headShotRatio",
    "rating": "rating",
    "pwRating": "pwRating",
    "flash": "flash",
    "flashTeammate": "flashTeammate",
    "flashSuccess": "flashSuccess",
    "mvpValue": "mvpValue",
    "twoKill": "twoKill",
    "threeKill": "threeKill",
    "fourKill": "fourKill",
    "fiveKill": "fiveKill",
    "vs1": "vs1",
    "vs2": "vs2",
    "vs3": "vs3",
    "vs4": "vs4",
    "vs5": "vs5",
    "dmgArmor": "dmgArmor",
    "dmgHealth": "dmgHealth",
    "adpr": "adpr",
    "fireCount": "fireCount",
    "hitCount": "hitCount",
    "rws": "rws",
    "pvpTeam": "pvpTeam",
    "ranks": "rank",
    "we": "we",
    "throwsCnt": "throwsCnt",
    "teamId": "teamId",
    "snipeNum": "snipeNum",
    "entryKill": "entryKill",
    "firstDeath": "firstDeath",
    "mvp": "mvp",
    "kast": "kast",
    "handGunKill": "handGunKill",
    "awpKill": "awpKill",
    "entryDeath": "entryDeath",
    "botKill": "botKill",
    "negKill": "negKill",
    "damage": "damage",
    "multiKills": "multiKills",
    "itemThrow": "itemThrow",
    "score": "score",
    "endGame": "endGame",
    "oldRank": "oldRank",
    "pvpScore": "pvpScore",
    "pvpScoreChange": "pvpScoreChange",
    "matchScore": "matchScore",
    "csMatchPlayerInterestList": "csMatchPlayerInterestList",
    "first": "first",
    "second": "second",
    "third": "third",
}

CHINESE_WEEKDAYS = {
    0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四',
    4: '星期五', 5: '星期六', 6: '星期日'
}

DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

def parse_datetime(ts: str) -> datetime:
    return datetime.strptime(ts, DATETIME_FMT)

def get_chinese_weekday(dt: datetime) -> str:
    return CHINESE_WEEKDAYS.get(dt.weekday(), '')

def cal_kda(kill: int, death: int, assist: int) -> float:
    return round((kill + assist) / (death or 1), 2)

def cal_win(team: str, win_team: str) -> int:
    return int(team == win_team)

def get_filtered_data(data: dict, toSteamId: str) -> dict:
    steam_id = str(toSteamId)
    base = data.get('base', {})
    win_team = base.get('winTeam')
    start_dt = parse_datetime(base.get('startTime', ''))
    end_dt = parse_datetime(base.get('endTime', ''))
    day_of_week = get_chinese_weekday(start_dt)
    players = [p for p in data.get('players', []) if str(p.get('playerId')) == steam_id]
    filtered_players = []
    for p in players:
        mapped = {out_key: p.get(in_key) for out_key, in_key in PLAYER_FIELD_MAP.items()}
        mapped['kda'] = cal_kda(int(p.get('kill', 0)), int(p.get('death', 0)), int(p.get('assist', 0)))
        mapped['win'] = cal_win(p.get('team'), win_team)
        filtered_players.append(mapped)
    result = {
        'matchId': base.get('matchId'),
        'map': base.get('map'),
        'mapEn': base.get('mapEn'),
        'startTime': start_dt,
        'endTime': end_dt,
        'duration': base.get('duration'),
        'winTeam': win_team,
        'score1': base.get('score1'),
        'score2': base.get('score2'),
        'team1PvpId': base.get('team1PvpId'),
        'team2PvpId': base.get('team2PvpId'),
        'pvpLadder': base.get('pvpLadder'),
        'mode': base.get('mode'),
        'dayOfWeek': day_of_week,
        'players': filtered_players,
    }
    logger.debug(result)
    return result