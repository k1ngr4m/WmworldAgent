from common.match_data_fetcher import new_fetcher
from config.params import userList, all_summoners_list

if __name__ == '__main__':
    fetcher = new_fetcher()
    summoner_name_list = userList.split(',')
    if summoner_name_list[0] == 'all':
        for i in range(len(all_summoners_list)):
            fetcher.fetch_player_data(all_summoners_list[i])
    else:
        for i in range(len(summoner_name_list)):
            fetcher.fetch_player_data(summoner_name_list[i])
