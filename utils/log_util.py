import logging
import time
import os
from config.config import log_path

# 控制台输出
STREAM = True

class LogUtil:
    def __init__(self):
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            log_name = '{}.log'.format(time.strftime("%Y_%m_%d", time.localtime()))
            log_path_file = os.path.join(log_path, log_name)
            fh = logging.FileHandler(log_path_file, encoding='utf-8', mode='a')
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            fh.close()
            if STREAM:
                fh_stream = logging.StreamHandler()
                fh_stream.setLevel(logging.DEBUG)
                fh_stream.setFormatter(formatter)
                self.logger.addHandler(fh_stream)

    def log(self):
        return self.logger

logger = LogUtil().log()