import os
import time
from dataclasses import dataclass

# 基本路径配置
abs_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(abs_path))
log_path = os.path.join(project_path, "log")

@dataclass
class DBConfig:
    host: str = "sh-cynosdbmysql-grp-2ywyko9q.sql.tencentcdb.com"
    user: str = "root"
    password: str = os.getenv("DB_PASSWORD", "ColayKD41!")
    database: str = "wmworld"
    port: int = 26754
    charset: str = "utf8"


@dataclass
class APIConfig:
    match_list_url: str = "https://api.wmpvp.com/api/csgo/home/match/list"
    match_detail_url: str = "https://api.wmpvp.com/api/v1/csgo/match"
    token: str = "befb16f88cc5044a4355f11c55010d5088be2c0d"
    data_source: int = 3


@dataclass
class AppConfig:
    data_count: int = 10
    max_pages: int = 1
    page_size: int = data_count
    batch_size: int = 100
    pvp_types: tuple = (0, 12, 41)
    seasons: list = None  # 延迟初始化
    all_summoners_list: list = None

    def __post_init__(self):
        # self.seasons = [f"S{i}" for i in range(1, 21)]
        self.seasons = ["recent"]
    @property
    def headers(self):
        timestamp = str(int(time.time()))
        return {
            'Host': 'api.wmpvp.com',
            'Accept': '*/*',
            'appversion': '3.4.3',
            'gameTypeStr': '2',
            'Accept-Language': 'zh-Hans-CN;q=1.0, zh-Hant-CN;q=0.9',
            'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
            'platform': 'ios',
            'token': self.api_config.token,
            't': timestamp,
            'User-Agent': 'esport-app/3.4.3 (com.wmzq.esportapp; build:1; iOS 17.6.1) Alamofire/5.9.1',
            'Connection': 'keep-alive',
            'gameType': '2',
            'device': 'tIPHq1725518646mFZInvTfjmf',
            'Content-Type': 'application/json'
        }

    @property
    def headers2(self):
        return {
            'Host': 'api.wmpvp.com',
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-site',
            'appversion': '3.4.3',
            'accessToken': self.api_config.token,
            'Accept-Language': 'zh-Hans-CN;q=1.0, zh-Hant-CN;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'platform': 'h5_ios',
            'Origin': 'https://news.wmpvp.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 EsportsApp Version=3.4.3 EsportsApp Version=3.4.3',
            'Referer': "https://news.wmpvp.com/",
            'Accept-Encoding': 'gzip, deflate, br',
            'device': 'tIPHq1725518646mFZInvTfjmf',
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
        }

    def __init__(self, db_config: DBConfig, api_config: APIConfig):
        self.db_config = db_config
        self.api_config = api_config
        self.__post_init__()
        self.all_summoners_list = [76561198828276659, 76561199005770156, 76561198800747248, 76561198398573973, 76561198812194679,
                          76561198856848006, 76561198359008979, 76561198163413971, 76561199511532518, 76561199270313195,
                          76561198843703833]