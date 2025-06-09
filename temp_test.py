import json

import requests
from config.itemList import item_name
import time
from config.params import token
import base64

# 获取当前时间的时间戳，单位为秒
timestamp = str(int(time.time()))

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

def test():
    url = "https://pwaweblogin.wmpvp.com/match-api/report?a=20000&r=873919&s=29b082059d5fb3bb57f0db3696a746469eaf11ca&t=1725551999425"
    headers = {
        'pwasteamid': '76561198828276659',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'no-cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) perfectworldarena/1.0.24090511 Chrome/80.0.3987.163 Electron/8.5.5 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN',
        'cookie': 'steam_cn_token=befb16f88cc5044a4355f11c55010d5088be2c0d; acw_tc=1a0c380d17255457706244764e003164b2309f9de759bfeb71905a78e3d0a2; path=/; HttpOnly; Max-Age=1800'
    }
    # payload = base64.b64decode(
    #     "eyJtYXRjaF9pZCI6IjkyMTg4MjgxNzQyNjQ3MTA5NTMiLCJzZWFzb24iOiJTMTciLCJ1aWQiOiI3NjU2MTE5ODgyODI3NjY1OSJ9")
    # print(payload)
    # response0 = requests.request("POST",url,headers=headers, data=payload)
    # print(response0.json())

    data = '{"match_id":"9218828174264710953","season":"S17","uid":"76561198828276659"}'
    result = requests.post(url=url, data=data, headers=headers)
    print(result.json())



def get_history():
    url = f'https://api.wmpvp.com/api/csgo/home/match/list'
    try:
        data = {
            "mySteamId": 76561198828276659,
            "pvpType": 41,  # {"官匹PRO":41}
            "toSteamId": 76561198828276659,
            "page": 1,
            "csgoSeasonId": "S17",  # "S16","S17","recent"
            "dataSource": 3,
            "pageSize": 50
        }
        result = requests.post(url=url, json=data, headers=HEADERS)
        print(result.text)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # get_history()
    test()
