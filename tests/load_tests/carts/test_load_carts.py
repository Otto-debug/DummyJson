import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.carts_api import CartsAPI
from utils.logger import get_logger


class CartsLoadTest(HttpUser):
    host = 'https://dummyjson.com'

    def on_start(self) -> None:
        self.carts_api = CartsAPI(self.client)

    @task(15)
    def test_get_carts(self):
        with self.carts_api.get_carts() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /carts | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /carts | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(10)
    def test_create_carts(self):
        cart_data = self.carts_api.generate_cart()
        with self.carts_api.create_cart(cart_data) as response:
            if response.status_code == 201:
                get_logger().info(f"✅ Карточка создана | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при создании карточки | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def test_update_carts(self):
        cart_id = self.carts_api.generate_cart_id()
        update_cart = self.carts_api.generate_update_cart()
        with self.carts_api.update_cart(cart_id, update_cart) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Карточка обновлена | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при обновлении карточки | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(1)
    def test_delete_cart(self):
        cart_id = self.carts_api.generate_cart_id()
        with self.carts_api.delete_carts(cart_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f"✅ Карточка удалена | {response.status_code}")
            else:
                get_logger().error(f"❌ Ошибка при удалении карточки | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

