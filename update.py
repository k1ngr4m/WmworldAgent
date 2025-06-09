from common.update_score_from_db import GameInfoFetcher
from config.params import update_version

if __name__ == '__main__':
    up = GameInfoFetcher()
    up.fetch_min_max_values()
    up.update_scores_in_database(update_version)
    up.fetch_min_max_values_total()
    up.update_scores_in_database_total(update_version)