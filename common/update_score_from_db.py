import time
from decimal import Decimal

from utils.mysqlutil import MysqlUtil
from utils.logutil import logger


class GameInfoFetcher:
    def __init__(self):
        self.mysql = MysqlUtil()
        self.game_modes = self.fetch_info('gameMode')
        self.game_versions = self.fetch_info('gameVersion')
        self.min_max_values_list = []
        self.min_max_values_list_total = []

    def fetch_info(self, key):
        info_list = []
        sql = f"SELECT DISTINCT {key} FROM tb_summoner_data_V2"
        res = self.mysql.get_fetchall(sql)
        for row in res:
            info = row.get(key)
            info_list.append(info)
        return info_list

    def convert_decimals_to_floats(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = self.convert_decimals_to_floats(value)
                elif isinstance(value, Decimal):
                    data[key] = float(value)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = self.convert_decimals_to_floats(data[i])
        return data

    def fetch_min_max_values(self):
        for version in self.game_versions:
            for mode in self.game_modes:
                sql = f"""
                    SELECT 'kda' AS column_name, MAX(kda) AS max_value, MIN(kda) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'damagePerMinute' AS column_name, MAX(damagePerMinute) AS max_value, MIN(damagePerMinute) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'damageTakenPerMinute' AS column_name, MAX(damageTakenPerMinute) AS max_value, MIN(damageTakenPerMinute) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'goldPerMinute' AS column_name, MAX(goldPerMinute) AS max_value, MIN(goldPerMinute) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'damageConversionRate' AS column_name, MAX(damageConversionRate) AS max_value, MIN(damageConversionRate) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'teamDamagePercentage' AS column_name, MAX(teamDamagePercentage) AS max_value, MIN(teamDamagePercentage) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'damageTakenOnTeamPercentage' AS column_name, MAX(damageTakenOnTeamPercentage) AS max_value, MIN(damageTakenOnTeamPercentage) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'killParticipation' AS column_name, MAX(killParticipation) AS max_value, MIN(killParticipation) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'effectiveHealAndShielding' AS column_name, MAX(effectiveHealAndShielding) AS max_value, MIN(effectiveHealAndShielding) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'totalHealsOnTeammates' AS column_name, MAX(totalHealsOnTeammates) AS max_value, MIN(totalHealsOnTeammates) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'doubleKills' AS column_name, MAX(doubleKills) AS max_value, MIN(doubleKills) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'tripleKills' AS column_name, MAX(tripleKills) AS max_value, MIN(tripleKills) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'quadraKills' AS column_name, MAX(quadraKills) AS max_value, MIN(quadraKills) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'pentaKills' AS column_name, MAX(pentaKills) AS max_value, MIN(pentaKills) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                """
                res = self.mysql.get_fetchall(sql)

                min_max_values_dict = {}
                for item in res:
                    if item['max_value'] is not None and item['min_value'] is not None:
                        min_max_values_dict['gameVersion'] = version
                        min_max_values_dict['gameMode'] = mode
                        min_max_values_dict[item['column_name'] + '_max'] = float(item['max_value'])
                        min_max_values_dict[item['column_name'] + '_min'] = float(item['min_value'])

                if min_max_values_dict:  # 如果字典不为空，则添加到列表中
                    self.min_max_values_list.append(min_max_values_dict)
        logger.info(self.min_max_values_list)

    def fetch_summoner_data(self, update_version):
        if update_version != 'all':
            query = f"""
                SELECT gameId, summonerId, kda, damagePerMinute, damageTakenPerMinute, goldPerMinute,
                       damageConversionRate, teamDamagePercentage, damageTakenOnTeamPercentage, killParticipation,
                       effectiveHealAndShielding, totalHealsOnTeammates,
                       doubleKills, tripleKills, quadraKills, pentaKills, gameMode,
                       gameVersion
                FROM tb_summoner_data_V2 WHERE gameVersion like '{update_version}%'
                """
        else:
            query = f"""
                SELECT gameId, summonerId, kda, damagePerMinute, damageTakenPerMinute, goldPerMinute,
                       damageConversionRate, teamDamagePercentage, damageTakenOnTeamPercentage, killParticipation,
                       effectiveHealAndShielding, totalHealsOnTeammates,
                       doubleKills, tripleKills, quadraKills, pentaKills, gameMode,
                       gameVersion
                FROM tb_summoner_data_V2
                """
        results = self.mysql.get_fetchall(query)
        data = []
        for row in results:
            data.append(row)
        data = self.convert_decimals_to_floats(data)
        return data

    def update_scores_in_database(self, update_version):
        from common.score_calculator import calculate_carry_score
        from common.score_calculator import calculate_tank_score
        from common.score_calculator import calculate_support_score
        data = self.fetch_summoner_data(update_version)
        for item in data:
            gameId = item['gameId']
            summonerId = item['summonerId']
            kda = item['kda']
            damage_per_minute = item['damagePerMinute']
            damage_taken_per_minute = item['damageTakenPerMinute']
            gold_per_minute = item['goldPerMinute']
            damage_conversion_rate = item['damageConversionRate']
            team_damage_percentage = item['teamDamagePercentage']
            damage_taken_on_team_percentage = item['damageTakenOnTeamPercentage']
            kill_participation = item['killParticipation']
            effective_heal_and_shielding = item['effectiveHealAndShielding']
            total_heals_on_teammates = item['totalHealsOnTeammates']
            double_kills = item['doubleKills']
            triple_kills = item['tripleKills']
            quadra_kills = item['quadraKills']
            penta_kills = item['pentaKills']
            game_mode = item['gameMode']
            game_version = item['gameVersion']

            carry_score = calculate_carry_score(kda, damage_per_minute, damage_taken_per_minute, gold_per_minute,
                                                damage_conversion_rate, team_damage_percentage, kill_participation,
                                                double_kills, triple_kills, quadra_kills, penta_kills, game_mode,
                                                game_version,
                                                min_max_values_list=self.min_max_values_list)

            tank_score = calculate_tank_score(kda, damage_per_minute, damage_taken_per_minute, gold_per_minute,
                                              damage_conversion_rate, team_damage_percentage,
                                              damage_taken_on_team_percentage,
                                              kill_participation, double_kills, triple_kills, quadra_kills, penta_kills,
                                              game_mode, game_version, min_max_values_list=self.min_max_values_list)

            support_score = calculate_support_score(kda, kill_participation, effective_heal_and_shielding,
                                                    total_heals_on_teammates, game_mode, game_version,
                                                    min_max_values_list=self.min_max_values_list)

            update_query = f"""
                UPDATE tb_summoner_data_V2
                SET carryScore = {carry_score}, tankScore = {tank_score}, supportScore = {support_score}
                WHERE gameId = {gameId} AND summonerId = {summonerId}
                AND (carryScore != {carry_score} or tankScore != {tank_score} or supportScore != {support_score})
            """
            affected_rows = self.mysql.sql_execute(update_query)
            if affected_rows != 0:
                logger.debug(update_query)
                logger.info(f"Updated {affected_rows}")

    def fetch_min_max_values_total(self):
        for version in self.game_versions:
            for mode in self.game_modes:
                sql = f"""
                    SELECT 'carryScore' AS column_name, MAX(carryScore) AS max_value, MIN(carryScore) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'tankScore' AS column_name, MAX(tankScore) AS max_value, MIN(tankScore) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                    UNION ALL
                    SELECT 'supportScore' AS column_name, MAX(supportScore) AS max_value, MIN(supportScore) AS min_value
                    FROM tb_summoner_data_V2
                    WHERE gameVersion = '{version}' AND gameMode = '{mode}'
                """
                res = self.mysql.get_fetchall(sql)
                min_max_values_dict = {}
                for item in res:
                    if item['max_value'] is not None and item['min_value'] is not None:
                        min_max_values_dict['gameVersion'] = version
                        min_max_values_dict['gameMode'] = mode
                        min_max_values_dict[item['column_name'] + '_max'] = float(item['max_value'])
                        min_max_values_dict[item['column_name'] + '_min'] = float(item['min_value'])
                if min_max_values_dict:  # 如果字典不为空，则添加到列表中
                    self.min_max_values_list_total.append(min_max_values_dict)
        logger.info(self.min_max_values_list_total)

    def fetch_summoner_data_total(self, update_version):
        if update_version != 'all':
            query = f"""
                SELECT gameId, summonerId, carryScore, tankScore, supportScore, gameMode,
                       gameVersion
                FROM tb_summoner_data_V2 WHERE gameVersion like '{update_version}%'
                """
        else:
            query = """
                SELECT gameId, summonerId, carryScore, tankScore, supportScore, gameMode,
                       gameVersion
                FROM tb_summoner_data_V2
                """

        results = self.mysql.get_fetchall(query)
        data = []
        for row in results:
            data.append(row)
        data = self.convert_decimals_to_floats(data)
        return data

    def update_scores_in_database_total(self, update_version):
        from common.score_calculator import calculate_total_score
        data = self.fetch_summoner_data_total(update_version)
        for item in data:
            gameId = item['gameId']
            summonerId = item['summonerId']
            carry_score = item['carryScore']
            tank_score = item['tankScore']
            support_score = item['supportScore']
            game_mode = item['gameMode']
            game_version = item['gameVersion']

            total_score, champion_classification = calculate_total_score(carry_score, tank_score, support_score,
                                                                         game_mode, game_version,
                                                                         min_max_values_list=self.min_max_values_list_total)

            update_query = f"""
                UPDATE tb_summoner_data_V2
                SET totalScore = {total_score}, championClassification = '{champion_classification}'
                WHERE gameId = {gameId} AND summonerId = {summonerId}
                AND (totalScore != {total_score} or championClassification != '{champion_classification}')
            """
            affected_rows = self.mysql.sql_execute(update_query)
            if affected_rows != 0:
                logger.debug(update_query)
                logger.info(f"Updated {affected_rows}")


if __name__ == '__main__':
    up = GameInfoFetcher()
    # up.fetch_min_max_values()
    # up.update_scores_in_database('all')
    up.fetch_min_max_values_total()
    up.update_scores_in_database_total('all')
