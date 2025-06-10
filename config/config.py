import os
import time

# 基本路径配置
abs_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(abs_path))
log_path = os.path.join(project_path, "log")

# 数据库配置
DB_CONFIG = {
    "host": "sh-cynosdbmysql-grp-2ywyko9q.sql.tencentcdb.com",
    "user": "root",
    "password": "ColayKD41!",
    "database": "wmworld",
    "port": 26754,
    "charset": "utf8"
}

# 数据表名
tb_summoner_info_name = '1'
tb_match_detail_name = 'cs_matches_detail'

# API 配置
token = "befb16f88cc5044a4355f11c55010d5088be2c0d"
timestamp = str(int(time.time()))
API_URL = {
    'MATCH_LIST': 'https://api.wmpvp.com/api/csgo/home/match/list',
    'MATCH_DETAIL': 'https://api.wmpvp.com/api/v1/csgo/match',
}
HEADERS = {
    'Host': 'api.wmpvp.com',
    'Accept': '*/*',
    'appversion': '3.4.3',
    'gameTypeStr': '2',
    'Accept-Language': 'zh-Hans-CN;q=1.0, zh-Hant-CN;q=0.9',
    'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
    'platform': 'ios',
    'token': token,
    't': timestamp,
    'User-Agent': 'esport-app/3.4.3 (com.wmzq.esportapp; build:1; iOS 17.6.1) Alamofire/5.9.1',
    'Connection': 'keep-alive',
    'gameType': '2',
    'device': 'tIPHq1725518646mFZInvTfjmf',
    'Content-Type': 'application/json'
}
HEADERS2 = {
    'Host': 'api.wmpvp.com',
    'Content-Type': 'application/json;charset=utf-8',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Site': 'same-site',
    'appversion': '3.4.3',
    'accessToken': token,
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

# 其他配置
data_count = 1000
userList = "all"
all_summoners_list = [76561198828276659, 76561199005770156, 76561198800747248, 76561198398573973, 76561198812194679, 76561198856848006, 76561198359008979, 76561198163413971, 76561199511532518, 76561199270313195, 76561198843703833]