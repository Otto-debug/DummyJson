from src.api.base_api import BaseAPI

class LoginAPI(BaseAPI):
    """Класс отвечающий за авторизацию"""

    def login(self, user_data: dict):
        return self.post(f'/auth/login', json=user_data)