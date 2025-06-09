import logging
from utils.log_util import logger
from utils.mysql_util import mysql
from config.settings import tb_match_detail_name


def update_summoner_data_to_db(match_data):
    # 插入数据
    # for game_data in match_data:
    game = match_data  # 因为 JSON 数据是一个包含单个元素的列表
    matchId = game['matchId']
    map = game['map']
    mapEn = game['mapEn']
    mapUrl = game['mapUrl']
    startTime = game['startTime']
    endTime = game['endTime']
    duration = game['duration']
    winTeam = game['winTeam']
    score1 = game['score1']
    score2 = game['score2']
    team1PvpId = game['team1PvpId']
    team2PvpId = game['team2PvpId']
    pvpLadder = game['pvpLadder']
    mode = game['mode']
    dayOfWeek = game['dayOfWeek']
    players = game.get('players', [])  # 获取参与者列表，若不存在则为空列表

    if players:  # 如果参与者列表不为空
        player = players[0]  # 获取第一个参与者
        playerId = player["playerId"]
        nickName = player["nickName"]
        team = player["team"]
        kills = player["kills"]
        deaths = player["deaths"]
        assists = player["assists"]
        headShot = player["headShot"]
        headShotRatio = player["headShotRatio"]
        rating = player["rating"]
        pwRating = player["pwRating"]
        flash = player["flash"]
        flashTeammate = player["flashTeammate"]
        flashSuccess = player["flashSuccess"]
        mvpValue = player["mvpValue"]
        twoKill = player["twoKill"]
        threeKill = player["threeKill"]
        fourKill = player["fourKill"]
        fiveKill = player["fiveKill"]
        vs1 = player["vs1"]
        vs2 = player["vs2"]
        vs3 = player["vs3"]
        vs4 = player["vs4"]
        vs5 = player["vs5"]
        dmgArmor = player["dmgArmor"]
        dmgHealth = player["dmgHealth"]
        adpr = player["adpr"]
        fireCount = player["fireCount"]
        hitCount = player["hitCount"]
        rws = player["rws"]
        pvpTeam = player["pvpTeam"]
        ranks = player["ranks"]
        we = player["we"]
        throwsCnt = player["throwsCnt"]
        teamId = player["teamId"]
        snipeNum = player["snipeNum"]
        entryKill = player["entryKill"]
        firstDeath = player["firstDeath"]
        mvp = player["mvp"]
        kda = player["kda"]
        win = player["win"]

        # 构建SQL插入语句示例
        insert_sql = f"""
        INSERT INTO {tb_match_detail_name} (
            matchId, map, mapEn, mapUrl, startTime, endTime, duration, winTeam, score1, score2,
            team1PvpId, team2PvpId, pvpLadder, mode, dayOfWeek,
            playerId, nickName, team, kills, deaths, assists, headShot, headShotRatio,
            rating, pwRating, flash, flashTeammate, flashSuccess, mvpValue, twoKill,
            threeKill, fourKill, fiveKill, vs1, vs2, vs3, vs4, vs5, dmgArmor, dmgHealth,
            adpr, fireCount, hitCount, rws, pvpTeam, ranks, we, throwsCnt, teamId,
            snipeNum, entryKill, firstDeath, mvp, kda, win
        ) VALUES (
            '{matchId}', '{map}', '{mapEn}', '{mapUrl}', '{startTime}', '{endTime}', {duration},
            {winTeam}, {score1}, {score2}, {team1PvpId}, {team2PvpId}, {pvpLadder}, '{mode}','{dayOfWeek}', 
            '{playerId}', '{nickName}', {team}, {kills}, {deaths}, {assists}, {headShot},
            {headShotRatio}, {rating}, {pwRating}, {flash}, {flashTeammate},
            {flashSuccess}, {mvpValue}, {twoKill}, {threeKill}, {fourKill}, {fiveKill},
            {vs1}, {vs2}, {vs3}, {vs4}, {vs5}, {dmgArmor}, {dmgHealth}, {adpr},
            {fireCount}, {hitCount}, {rws}, {pvpTeam}, {ranks}, {we}, {throwsCnt},
            {teamId}, {snipeNum}, {entryKill}, {firstDeath}, {mvp}, {kda}, {win}
        );
        """

        logger.info(insert_sql)
        # 执行 SQL 语句
        mysql.sql_execute(insert_sql)
    logger.info("SQL执行完毕")
