import pymysql
from utils.log_util import logger
from config.settings import DB_CONFIG


class MysqlUtil:
    def __init__(self):
        self.db = pymysql.connect(**DB_CONFIG)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取单条数据
    def get_fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 获取多条数据
    def get_fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def sql_execute(self, sql, params=None):
        """支持带参数的SQL执行"""
        try:
            if self.db and self.cursor:
                if params:
                    self.cursor.execute(sql, params)
                else:
                    self.cursor.execute(sql)
                affected_rows = self.cursor.rowcount
                self.db.commit()
                return affected_rows
        except Exception as e:
            self.db.rollback()
            logger.error(f"SQL执行错误: {sql}")
            logger.error(f"错误详情: {e}")
            return False

    def executemany(self, sql, params_list):
        """新增批量执行方法"""
        try:
            if self.db and self.cursor:
                self.cursor.executemany(sql, params_list)
                affected_rows = self.cursor.rowcount
                self.db.commit()
                return affected_rows
        except Exception as e:
            self.db.rollback()
            logger.error(f"批量执行错误: {sql}")
            logger.error(f"错误详情: {e}")
            return False

    def delete_data(self, delete_query):
        try:
            self.cursor.execute(delete_query)
            affected_rows = self.cursor.rowcount  # 获取受影响的行数
            self.db.commit()
            logger.info(f"删除成功，受影响的行数: {affected_rows}")
            return affected_rows
        except Exception as e:
            self.db.rollback()
            logger.error("删除失败:", e)

    @staticmethod
    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()

mysql = MysqlUtil()