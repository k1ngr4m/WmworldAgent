# coding = utf-8
import os
from config.params import database


# 获取文件的绝对路径
abs_path = os.path.abspath(__file__)
# print(abs_path)

# 获取文件所在目录的上一级目录，也就是根目录
project_path = os.path.dirname(os.path.dirname(abs_path))
# print(project_path)

# 获取log日志目录的全路径
_log_path = project_path + os.sep + "log"

# 数据库配置信息
DB_CONFIG = {
    "host": "sh-cynosdbmysql-grp-2ywyko9q.sql.tencentcdb.com",
    "user": "root",
    "password": "ColayKD41!",
    "database": database,
    "port": 26754,
    "charset": "utf8"
}


tb_summoner_info_name = '1'
tb_match_detail_name = 'cs_matches_detail'


# 返回日志目录
def get_log_path():
    return _log_path


# 占位用，勿删除
class DynamicParam:
    pass


# 测试代码
if __name__ == '__main__':
    print(get_log_path())
