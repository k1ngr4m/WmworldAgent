import requests
from utils.log_util import logger

class RequestUtil:
    def __init__(self):
        self.session = requests.Session()

    def post_json(self, url, headers, payload=None):
        try:
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request to {url} failed: {str(e)}")
        except ValueError as ve:
            logger.error(f"JSON decode error: {str(ve)}")
        return None