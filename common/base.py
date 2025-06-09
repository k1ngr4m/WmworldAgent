import requests

from config.params import data_count
from config.requestparams import API_URL, HEADERS1, HEADERS2
from utils.logutil import logger
from common.update_db import update_summoner_data_to_db
# from utils.mysqlutil import MysqlUtil

from common.score_calculator import get_filtered_data

data_count = int(data_count)

def determine_range_count(count):
    # if count < 100:
    #     return 10
    # elif 100 <= count < 400:
    #     return 20
    # else:
    #     return 40
    return count


class Base:
    def __init__(self):
        self.session = requests.Session()

    # 获取玩家对战历史记录
    def get_match_history(self, toSteamId):
        url = f'https://api.wmpvp.com/api/csgo/home/match/list'
        range_count = determine_range_count(data_count)
        match_list = []

        for i in range(data_count // range_count):
            try:
                data = {
                    "mySteamId": 76561198828276659,
                    "pvpType": 41,  # {"官匹PRO":41},{"天梯组排对局":12},{"天梯组排对局": 0},{"PVP自定义":14}
                    "toSteamId": toSteamId,
                    "page": i + 1,
                    "csgoSeasonId": "recent",  # "S16","S17","recent"
                    "dataSource": 3,
                    "pageSize": range_count
                }
                result = requests.post(url=url, json=data, headers=HEADERS1).json()
                if result.get('statusCode') == 0 and 'data' in result:
                    filtered_data = result['data']['matchList']
                    for j in range(len(filtered_data)):
                        matchId = filtered_data[j]['matchId']
                        match_list.append(matchId)
                    logger.info(f"matchList:{match_list}")
                    return match_list
                else:
                    logger.error(result)
            except Exception as e:
                logger.error(e)

    def get_match_detail(self, matchList, toSteamId):
        url = f'https://api.wmpvp.com/api/v1/csgo/match'
        for matchId in matchList:
            # try:
            data = {
                "matchId": matchId,
                "platform": "admin",
                "dataSource": 3
            }
            result = requests.post(url=url, json=data, headers=HEADERS2).json()
            if result.get('statusCode') == 0 and 'data' in result:
                data = result['data']
                logger.info(f'matchDetail：{data}')
                filtered_data = get_filtered_data(data, toSteamId)
                if filtered_data:
                    del_count = update_summoner_data_to_db(filtered_data)
                    len_count = len(filtered_data)
                    save_count = len_count - del_count
                    # count += save_count
                    logger.info(
                        f'此次  共获取 {len_count} 条数据，在数据库中删除 {del_count} 条重复数据，已保存 {save_count} 条数据')
            else:
                logger.error(result)
            # except Exception as e:
            #     logger.error(e)

    def get_data(self, toSteamId):
        matchLists = self.get_match_history(toSteamId)
        self.get_match_detail(matchLists, toSteamId)


if __name__ == '__main__':
    base = Base()
    match_list = base.get_match_history(76561198163413971)
    base.get_match_detail(match_list, 76561198163413971)
