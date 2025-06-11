import time

import requests
from typing import Optional, Dict, List

from config.config import AppConfig
from utils.log_util import logger

class APIService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.session = requests.Session()
        self.retries = 3
        self.backoff_factor = 0.5

    def _request_with_retry(self, method: str, url: str, headers: dict, payload: dict = None) -> Optional[dict]:
        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method,
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10 + attempt * 2
                )
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                logger.warning(f"API请求失败 (尝试 {attempt+1}/{self.retries}): {e}")
                if attempt < self.retries - 1:
                    sleep_time = self.backoff_factor * (2 ** attempt)
                    time.sleep(sleep_time)
                else:
                    logger.error(f"API请求最终失败: {url} {payload}")
        return None

    def get_match_list(self, steam_id: str) -> List[int]:
        """获取指定玩家的比赛ID列表"""
        match_ids = []
        headers = self.config.headers

        for season in self.config.seasons:
            for pvp_type in self.config.pvp_types:
                page = 1
                while True:
                    if self.config.max_pages and page > self.config.max_pages:
                        logger.debug(f"达到最大页数限制: {season}-{pvp_type}")
                        break

                    payload = {
                        "mySteamId": 76561198828276659,  # 示例ID，实际可能需要调整
                        "pvpType": pvp_type,
                        "toSteamId": steam_id,
                        "page": page,
                        "csgoSeasonId": season,
                        "dataSource": self.config.api_config.data_source,
                        "pageSize": self.config.page_size,
                    }

                    logger.debug(f"请求比赛列表: season={season}, pvp={pvp_type}, page={page}")
                    data = self._request_with_retry(
                        "POST",
                        self.config.api_config.match_list_url,
                        headers,
                        payload
                    )

                    # 检查响应状态
                    if not data or data.get('statusCode') != 0:
                        logger.warning(f"无效响应: season={season}, pvp={pvp_type}, page={page}")
                        break

                    matches = data.get('data', {}).get('matchList', [])
                    if not matches:
                        logger.debug(f"无更多数据: season={season}, pvp={pvp_type}")
                        break

                    # 提取比赛ID
                    ids = [m['matchId'] for m in matches]
                    match_ids.extend(ids)
                    logger.debug(f"获取 {len(ids)} 个比赛ID")

                    # 检查是否还有更多页面
                    if len(matches) < self.config.page_size:
                        break

                    page += 1

        logger.info(f"为玩家 {steam_id} 获取到 {len(match_ids)} 个比赛ID")
        return match_ids

    def get_match_details(self, match_id: int) -> Optional[Dict]:
        """获取指定比赛的详细数据"""
        headers = self.config.headers2
        payload = {
            "matchId": match_id,
            "platform": "admin",
            "dataSource": self.config.api_config.data_source
        }

        logger.debug(f"请求比赛详情: match_id={match_id}")
        response = self._request_with_retry(
            "POST",
            self.config.api_config.match_detail_url,
            headers,
            payload
        )

        if not response or response.get('statusCode') != 0:
            logger.warning(f"无效的比赛详情响应: match_id={match_id}")
            return None

        return response.get('data')