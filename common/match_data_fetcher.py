import itertools
from typing import List, Optional
from utils.log_util import logger
from utils.request_util import RequestUtil
from config.config import data_count, API_URL, HEADERS, HEADERS2
from common.score_calculator import get_filtered_data
from common.update_db import update_summoner_data_to_db

class MatchDataFetcher:
    PVP_TYPES = (0, 12, 41)
    SEASONS = [f"S{i}" for i in range(1, 21)]
    PAGE_SIZE = int(data_count)
    MAX_PAGES = 1

    def __init__(self):
        self.request_util = RequestUtil()

    def _fetch_json(self, url: str, headers: dict, payload: dict) -> Optional[dict]:
        try:
            res = self.request_util.post_json(url, headers, payload)
            if res and res.get('statusCode') == 0:
                return res.get('data')
        except Exception as e:
            logger.error(f"请求失败 {url} {payload}: {e}")
        return None

    def get_match_history(self, steam_id: str) -> List[int]:
        match_ids: List[int] = []
        for season in self.SEASONS:
            for pvp in self.PVP_TYPES:
                page = 1
                while True:
                    if self.MAX_PAGES and page > self.MAX_PAGES:
                        break
                    payload = {
                        "mySteamId": 76561198828276659,
                        "pvpType": pvp,
                        "toSteamId": steam_id,
                        "page": page,
                        "csgoSeasonId": season,
                        "dataSource": 3,
                        "pageSize": self.PAGE_SIZE,
                    }
                    data = self._fetch_json(API_URL['MATCH_LIST'], HEADERS, payload)
                    matches = data.get('matchList', []) if data else []
                    if not matches:
                        logger.info(f"{season}#{pvp} page={page} 无数据，切换到下一个组合")
                        break
                    ids = [m['matchId'] for m in matches]
                    match_ids.extend(ids)
                    logger.debug(f"{season}#{pvp} page={page} fetched {len(ids)} records")
                    page += 1
        logger.info(f"总共获取 matchId: {len(match_ids)} 条，组合({len(self.SEASONS)}×{len(self.PVP_TYPES)})")
        return match_ids

    def fetch_match_details(self, match_id: int) -> Optional[dict]:
        payload = {
            "matchId": match_id,
            "platform": "admin",
            "dataSource": 3
        }
        return self._fetch_json(API_URL['MATCH_DETAIL'], HEADERS2, payload)

    def process_player(self, steam_id: str) -> None:
        ids = self.get_match_history(steam_id)
        for mid in ids:
            detail = self.fetch_match_details(mid)
            if not detail:
                logger.warning(f"详情为空: matchId={mid}")
                continue
            filtered = get_filtered_data(detail, steam_id)
            if not filtered.get('players'):
                logger.debug(f"无目标玩家数据: matchId={mid}")
                continue
            update_summoner_data_to_db(filtered)

def new_fetcher() -> MatchDataFetcher:
    return MatchDataFetcher()