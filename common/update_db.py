import time
from utils.mysql_util import mysql
from utils.log_util import logger
from config.config import tb_match_detail_name

COLUMNS = [
    "matchId", "map", "mapEn", "startTime", "endTime", "duration", "winTeam",
    "score1", "score2", "team1PvpId", "team2PvpId", "pvpLadder", "mode",
    "dayOfWeek",
    "playerId", "nickName", "team", "kills", "deaths", "assists", "headShot",
    "headShotCount", "headShotRatio", "rating", "pwRating", "flash",
    "flashTeammate", "flashSuccess", "mvpValue", "twoKill", "threeKill",
    "fourKill", "fiveKill", "vs1", "vs2", "vs3", "vs4", "vs5", "dmgArmor",
    "dmgHealth", "adpr", "fireCount", "hitCount", "rws", "pvpTeam", "ranks",
    "we", "throwsCnt", "teamId", "snipeNum", "entryKill", "firstDeath", "mvp",
    "kda", "kast", "handGunKill", "awpKill", "entryDeath", "botKill",
    "negKill", "damage", "multiKills", "itemThrow", "score", "endGame",
    "oldRank", "pvpScore", "pvpScoreChange", "matchScore", "win"
]

PLACEHOLDERS = ", ".join(f"%({col})s" for col in COLUMNS)
COLUMN_LIST = ", ".join(COLUMNS)
BATCH_SIZE = 100
duplicates = ", ".join(f"{col}=VALUES({col})" for col in COLUMNS)
ON_DUPLICATE = f"ON DUPLICATE KEY UPDATE {duplicates}"
INSERT_SQL = f"""
INSERT INTO {tb_match_detail_name} ({COLUMN_LIST})
VALUES ({PLACEHOLDERS})
{ON_DUPLICATE}
"""

def _bulk_insert(batch):
    inserted = 0
    try:
        rows = mysql.executemany(INSERT_SQL, batch)
        if rows is False:
            raise RuntimeError("executemany 返回 False")
        inserted += rows
        logger.debug(f"批量插入成功：{rows} 条")
    except Exception as e:
        logger.warning(f"批量插入失败（{e}），切换单条插入")
        for rec in batch:
            try:
                res = mysql.sql_execute(INSERT_SQL, rec)
                if res:
                    inserted += 1
                else:
                    logger.error(f"单条插入失败，playerId={rec.get('playerId')}")
            except Exception as e2:
                logger.error(f"单条插入异常，playerId={rec.get('playerId')}：{e2}")
    return inserted

def update_summoner_data_to_db(match_data):
    try:
        players = match_data.get("players") or []
        if not players:
            logger.info("没有玩家数据，跳过插入")
            return
        common_data = {k: match_data[k] for k in (
            "matchId", "map", "mapEn", "startTime", "endTime", "duration",
            "winTeam", "score1", "score2", "team1PvpId", "team2PvpId",
            "pvpLadder", "mode", "dayOfWeek"
        )}
        batch_data = [{**common_data, **player} for player in players]
        start = time.time()
        total_inserted = 0
        for i in range(0, len(batch_data), BATCH_SIZE):
            batch = batch_data[i : i + BATCH_SIZE]
            total_inserted += _bulk_insert(batch)
        elapsed = time.time() - start
        logger.info(f"共插入 {total_inserted}/{len(players)} 条，用时 {elapsed:.2f}s")
    except KeyError as e:
        logger.error(f"数据字段缺失：{e}")
    except Exception as e:
        logger.error(f"更新比赛数据异常：{e}")