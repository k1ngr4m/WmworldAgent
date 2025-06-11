from typing import List, Dict

import pymysql
from contextlib import contextmanager
from utils.log_util import logger
from config.config import DBConfig


class MySQLRepository:
    def __init__(self, config: DBConfig):
        self.config = config
        self.pool = self._create_connection_pool()

    def _create_connection_pool(self):
        # 使用DBUtils创建连接池
        from dbutils.pooled_db import PooledDB
        return PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=2,
            **self.config.__dict__
        )

    @contextmanager
    def get_cursor(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def bulk_insert_match_details(self, table_name: str, data: List[Dict], batch_size: int = 100):
        if not data:
            return 0

        columns = list(data[0].keys())
        placeholders = ", ".join(["%s"] * len(columns))
        columns_str = ", ".join(columns)
        duplicates = ", ".join([f"{col}=VALUES({col})" for col in columns])

        sql = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {duplicates}
        """

        total_inserted = 0
        with self.get_cursor() as cursor:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                try:
                    cursor.executemany(sql, [tuple(item.values()) for item in batch])
                    total_inserted += cursor.rowcount
                except pymysql.Error as e:
                    logger.error(f"批量插入失败: {e}")
                    # 退化为单条插入
                    for item in batch:
                        try:
                            cursor.execute(sql, tuple(item.values()))
                            total_inserted += 1
                        except pymysql.Error as e2:
                            logger.error(f"单条插入失败: {e2}")

        return total_inserted
