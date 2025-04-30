from src.api.base_api import BaseAPI

class UsersAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /users"""

    def get_user(self, user_id):
        return self.get(f"/users/{user_id}")

    def create_user(self, user_data: dict):
        return self.post('/users/add', json=user_data)

    def update_user(self, user_id, user_data: dict):
        return self.put(f"/users/{user_id}", json=user_data)

    def delete_user(self, user_id):
        return self.delete(f'/users/{user_id}')