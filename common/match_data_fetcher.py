from typing import Optional
from common.services import APIService
from utils.repositories import MySQLRepository
from common.models import MatchDetail, Player, MatchBase
from config.config import AppConfig
from utils.log_util import logger
from datetime import datetime
import time


class MatchDataFetcher:
    def __init__(self, api_service: APIService, db_repo: MySQLRepository, config: AppConfig):
        self.api_service = api_service
        self.db_repo = db_repo
        self.config = config

    def process_player(self, steam_id: str) -> None:
        """处理单个玩家的比赛数据"""
        logger.info(f"开始处理玩家 {steam_id} 的比赛数据")
        start_time = time.time()

        try:
            match_ids = self.api_service.get_match_list(steam_id)
            total_matches = len(match_ids)
            processed = 0

            for match_id in match_ids:
                match_detail = self._fetch_and_process_match(match_id, steam_id)
                if match_detail:
                    self._save_match_details(match_detail)
                    processed += 1

            elapsed = time.time() - start_time
            logger.info(f"完成玩家 {steam_id} 处理: {processed}/{total_matches} 场比赛, 用时 {elapsed:.2f}秒")
        except Exception as e:
            logger.error(f"处理玩家 {steam_id} 时发生错误: {e}")

    def _fetch_and_process_match(self, match_id: int, steam_id: str) -> Optional[MatchDetail]:
        """获取并处理单场比赛数据"""
        raw_data = self.api_service.get_match_details(match_id)
        if not raw_data:
            logger.warning(f"未获取到比赛详情: match_id={match_id}")
            return None

        try:
            return MatchDetailProcessor.process(raw_data, steam_id)
        except Exception as e:
            logger.error(f"处理比赛数据失败 {match_id}: {e}")
            return None

    def _save_match_details(self, match_detail: MatchDetail) -> None:
        """保存比赛数据到数据库"""
        try:
            db_data = match_detail.to_db_dict()
            inserted = self.db_repo.bulk_insert_match_details(
                "cs_matches_detailV2",
                db_data,
                self.config.batch_size
            )
            logger.debug(f"保存比赛数据成功: match_id={match_detail.base.match_id}, 插入{inserted}条玩家记录")
        except Exception as e:
            logger.error(f"保存比赛数据失败: {e}")


class MatchDetailProcessor:
    """比赛详情数据处理工具类"""

    CHINESE_WEEKDAYS = {
        0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四',
        4: '星期五', 5: '星期六', 6: '星期日'
    }

    @staticmethod
    def parse_datetime(ts: str) -> datetime:
        """解析时间字符串"""
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            logger.warning(f"无效的时间格式: {ts}")
            return datetime.now()

    @staticmethod
    def get_chinese_weekday(dt: datetime) -> str:
        """获取中文星期"""
        return MatchDetailProcessor.CHINESE_WEEKDAYS.get(dt.weekday(), '未知')

    @staticmethod
    def cal_kda(kills: int, deaths: int, assists: int) -> float:
        """计算KDA值"""
        return round((kills + assists) / max(deaths, 1), 2)

    @staticmethod
    def cal_win(team: str, win_team: str) -> int:
        """判断是否获胜"""
        return 1 if team == win_team else 0

    @staticmethod
    def process(raw_data: dict, steam_id: str) -> MatchDetail:
        """处理原始比赛数据"""
        base_data = raw_data.get('base', {})
        players_data = raw_data.get('players', [])

        # 处理基础比赛信息
        start_time = MatchDetailProcessor.parse_datetime(base_data.get('startTime', ''))
        end_time = MatchDetailProcessor.parse_datetime(base_data.get('endTime', ''))

        match_base = MatchBase(
            match_id=base_data.get('matchId'),
            map_name=base_data.get('map'),
            map_en=base_data.get('mapEn'),
            start_time=start_time,
            end_time=end_time,
            duration=base_data.get('duration', 0),
            win_team=base_data.get('winTeam', ''),
            score1=base_data.get('score1', 0),
            score2=base_data.get('score2', 0),
            team1_pvp_id=base_data.get('team1PvpId'),
            team2_pvp_id=base_data.get('team2PvpId'),
            pvp_ladder=base_data.get('pvpLadder'),
            mode=base_data.get('mode'),
            day_of_week=MatchDetailProcessor.get_chinese_weekday(start_time)
        )

        # 处理玩家数据
        players = []
        steam_id_str = str(steam_id)

        for player in players_data:
            if str(player.get('playerId')) != steam_id_str:
                continue

            kills = player.get('kill', 0)
            deaths = player.get('death', 0)
            assists = player.get('assist', 0)

            p = Player(
                playerId=player.get('playerId'),
                nickName=player.get('nickName', ''),
                team=player.get('team', ''),
                kills=kills,
                deaths=deaths,
                assists=assists,
                headShot=player.get('headShot'),
                headShotCount=player.get('headShotCount'),
                headShotRatio=player.get('headShotRatio'),
                rating=player.get('rating', 0.0),
                pwRating=player.get('pwRating', 0.0),
                flash=player.get('flash', 0),
                flashTeammate=player.get('flashTeammate', 0),
                flashSuccess=player.get('flashSuccess', 0),
                mvpValue=player.get('mvpValue', 0.0),
                twoKill=player.get('twoKill', 0),
                threeKill=player.get('threeKill', 0),
                fourKill=player.get('fourKill', 0),
                fiveKill=player.get('fiveKill', 0),
                vs1=player.get('vs1', 0),
                vs2=player.get('vs2', 0),
                vs3=player.get('vs3', 0),
                vs4=player.get('vs4', 0),
                vs5=player.get('vs5', 0),
                dmgArmor=player.get('dmgArmor', 0),
                dmgHealth=player.get('dmgHealth', 0),
                adpr=player.get('adpr', 0.0),
                fireCount=player.get('fireCount', 0),
                hitCount=player.get('hitCount', 0),
                rws=player.get('rws', 0.0),
                pvpTeam=player.get('pvpTeam', ''),
                ranks=player.get('ranks', 0),
                we=player.get('we', 0.0),
                throwsCnt=player.get('throwsCnt', 0),
                teamId=player.get('teamId', ''),
                snipeNum=player.get('snipeNum', 0),
                entryKill=player.get('entryKill', 0),
                firstDeath=player.get('firstDeath', 0),
                mvp=player.get('mvp', 0),
                kast=player.get('kast', 0.0),
                handGunKill=player.get('handGunKill', 0),
                awpKill=player.get('awpKill', 0),
                entryDeath=player.get('entryDeath', 0),
                botKill=player.get('botKill', 0),
                negKill=player.get('negKill', 0),
                damage=player.get('damage', 0),
                multiKills=player.get('multiKills', 0),
                itemThrow=player.get('itemThrow', 0),
                score=player.get('score', 0),
                endGame=player.get('endGame', False),
                oldRank=player.get('oldRank', ''),
                pvpScore=player.get('pvpScore', 0.0),
                pvpScoreChange=player.get('pvpScoreChange', 0.0),
                matchScore=player.get('matchScore', 0.0),
                kda=MatchDetailProcessor.cal_kda(kills, deaths, assists),
                win=MatchDetailProcessor.cal_win(player.get('team'), base_data.get('winTeam', ''))
            )
            players.append(p)

        return MatchDetail(base=match_base, players=players)