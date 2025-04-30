import logging
from requests import Response
import requests

logger = logging.getLogger("API")

class BaseAPI:
    """Базовый класс API"""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {"Content-Type": 'application/json'} # Заголовки
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> Response | None:
        """Отправляет http-запросы к api"""

        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("headers", self.headers)
        kwargs.setdefault("timeout", self.timeout)

        try:
            logger.info(f"Выполнено {method}-запроса к {url} с параметрами {kwargs}")
            response = self.session.request(method, url, **kwargs)
            logger.info(f"Статус код: {response.status_code}")

            if response.status_code >= 400:
                logger.error(f"Ошибка запроса: {response.status_code} - {response.text}")
            return response
        except requests.RequestException as e:
            logger.error(f"Ошибка запроса {e}", exc_info=True)
            return None # Возвращаем в случае ошибки

    def get(self, endpoint: str, **kwargs) -> Response | None:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response | None:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response | None:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response | None:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response | None:
        return self.request("DELETE", endpoint, **kwargs)
