import requests

from utils.log_util import logger


class RequestUtil:
    """HTTP 请求工具类"""

    def __init__(self):
        self.session = requests.Session()

    def post_json(self, url, headers, payload=None):
        """
        发送 JSON POST 请求
        :param url: 请求URL
        :param headers: 请求头
        :param payload: 请求体数据
        :return: 响应数据（字典）或 None
        """
        try:
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()  # 检查HTTP状态码
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request to {url} failed: {str(e)}")
        except ValueError as ve:
            logger.error(f"JSON decode error: {str(ve)}")
        return None