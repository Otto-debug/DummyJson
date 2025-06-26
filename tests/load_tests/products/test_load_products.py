import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.products_api import ProductsAPI
from utils.logger import get_logger

class ProductsLoadTest(HttpUser):
    host = "https://dummyjson.com"

    def on_start(self) -> None:
        self.products_api = ProductsAPI(self.client)

    @task(15)
    def get_products(self):
        with self.products_api.get_products() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /products | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /response | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(10)
    def create_products(self):
        product_data = self.products_api.generate_fake_product()
        with self.products_api.create_products(product_data) as response:
            if response.status_code == 201:
                get_logger().info(f"✅ Продукт создан | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка создания продукта | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def update_products(self):
        product_id = self.products_api.generate_random_product_id()
        update_product = self.products_api.generate_update_product()
        with self.products_api.updt_product(product_id, update_product) as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Продукт обновлён | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка обновлении продукта | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(1)
    def delete_products(self):
        product_id = self.products_api.generate_random_product_id()
        with self.products_api.delete_products(product_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f'✅ Продукт удалён | Код: {response.status_code}')
            else:
                get_logger().error(f"❌ Ошибка при удалении продукта | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")
