from common.base import Base
from config.params import userList
from config.settings import all_summoners_list
from common.update_score_from_db import GameInfoFetcher

if __name__ == '__main__':
    base = Base()
    summoner_name_list = userList.split(',')
    if summoner_name_list[0] == 'all':
        for i in range(len(all_summoners_list)):
            base.get_data(all_summoners_list[i])
    else:
        for i in range(len(summoner_name_list)):
            base.get_data(summoner_name_list[i])
