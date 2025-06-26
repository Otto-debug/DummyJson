import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.user_api import UsersAPI
from utils.logger import get_logger

class UserLoadTest(HttpUser):
    host = "https://dummyjson.com"

    def on_start(self):
        self.user_api = UsersAPI(self.client)

    @task(10)
    def test_get_users(self):
        with self.user_api.get_all_users() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /users | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /users | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(7)
    def test_create_user(self):
        fake_user = self.user_api.generate_fake_user()
        with self.user_api.create_user(fake_user) as response:
            if response.status_code == 201:
                get_logger().info(f"✅ Пользователь создан | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка создания пользователя | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def test_update_user(self):
        user_id = self.user_api.generate_id_user()
        update_data = self.user_api.generate_user_update()
        with self.user_api.updt_user(user_id, update_data) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Пользователь обновлён | {response.json}")
            else:
                get_logger().error(f"❌ Ошибка при обновлении пользователя | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(3)
    def test_delete_user(self):
        user_id = self.user_api.generate_id_user()
        with self.user_api.delete_user(user_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f'✅ Пользователь удалён | Код: {response.status_code}')
            else:
                get_logger().error(f"❌ Ошибка при удалении пользователя | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")
