import time
from config.params import token

# 获取当前时间的时间戳，单位为秒
timestamp = str(int(time.time()))

API_URL = {
    'get_history_url': 'https://api.wmpvp.com/api/csgo/home/match/list',
    'get_match_url': 'https://api.wmpvp.com/api/v1/csgo/match',
}
HEADERS1 = {
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
