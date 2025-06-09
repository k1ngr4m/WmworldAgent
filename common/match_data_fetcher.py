import requests
from config.params import data_count
from config.requestparams import API_URL, HEADERS, HEADERS2
from utils.log_util import logger
from common.update_db import update_summoner_data_to_db
from common.score_calculator import get_filtered_data
from utils.request_util import RequestUtil


class MatchDataFetcher:
    def __init__(self):
        self.request_util = RequestUtil()
        self.data_count = int(data_count)

    @staticmethod
    def determine_range_count(count):
        # if count < 100:
        #     return 10
        # elif 100 <= count < 400:
        #     return 20
        # else:
        #     return 40
        return count

    def _fetch_match_page(self, steam_id, page, range_count, pvpType, csgoSeasonId):
        """获取单页比赛历史数据"""
        url = 'https://api.wmpvp.com/api/csgo/home/match/list'
        payload = {
            "mySteamId": 76561198828276659,
            "pvpType": pvpType,
            "toSteamId": steam_id,
            "page": page,
            "csgoSeasonId": csgoSeasonId,
            "dataSource": 3,
            "pageSize": range_count
        }
        print(payload)
        result = self.request_util.post_json(url, HEADERS, payload)
        if result and result.get('statusCode') == 0:
            return result.get('data', {}).get('matchList', [])
        return []

    def get_match_history(self, steam_id):
        """获取玩家完整的对战历史记录"""
        range_count = self.determine_range_count(self.data_count)
        total_pages = (self.data_count + range_count - 1) // range_count  # 向上取整
        match_ids = []
        pvp_type = [0, 12, 41]
        csgoSeasonId = []
        # for i in range(1,21):
        #     seasonId = f"S{i}"
        #     csgoSeasonId.append(seasonId)
        csgoSeasonId.append("recent")
        for page in range(1, total_pages + 1):
            for seasonId in csgoSeasonId:
                for pvp in pvp_type:
                    matches = self._fetch_match_page(steam_id, page, range_count, pvp, seasonId)
                    # if not matches:
                    #     break

                    match_ids.extend(match['matchId'] for match in matches)
                    logger.debug(f"Page {page}: Added {len(matches)} matches")

        logger.info(f"Total matches fetched: {len(match_ids)}")
        return match_ids

    def _fetch_match_details(self, match_id):
        """获取单场比赛详情"""
        url = 'https://api.wmpvp.com/api/v1/csgo/match'
        payload = {
            "matchId": match_id,
            "platform": "admin",
            "dataSource": 3
        }

        result = self.request_util.post_json(url, HEADERS2, payload)
        if result and result.get('statusCode') == 0:
            return result.get('data')
        return None

    def process_match_details(self, match_ids, steam_id):
        """处理并保存比赛详情数据"""
        for match_id in match_ids:
            match_data = self._fetch_match_details(match_id)
            if not match_data:
                logger.warning(f"No data for match ID: {match_id}")
                continue

            filtered_data = get_filtered_data(match_data, steam_id)
            if not filtered_data:
                logger.info(f"No filtered data for match ID: {match_id}")
                continue

            update_summoner_data_to_db(filtered_data)

    def fetch_player_data(self, steam_id):
        """获取并处理玩家数据的主入口"""
        match_ids = self.get_match_history(steam_id)
        if match_ids:
            self.process_match_details(match_ids, steam_id)
        else:
            logger.warning(f"No matches found for Steam ID: {steam_id}")

def new_fetcher():
    return MatchDataFetcher()