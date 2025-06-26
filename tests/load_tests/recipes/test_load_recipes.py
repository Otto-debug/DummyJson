import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.recipes_api import RecipesAPI
from utils.logger import get_logger

class TestLoadRecipes(HttpUser):
    host = 'https://dummyjson.com'

    def on_start(self) -> None:
        self.recipes_api = RecipesAPI(self.client)

    @task(15)
    def test_get_recipes(self):
        with self.recipes_api.get_recipes() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /recipes | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /recipes | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(10)
    def test_create_recipes(self):
        recipes_data = self.recipes_api.generate_recipes()
        with self.recipes_api.create_recipes(recipes_data) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Рецепт создан | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при создании рецепта | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def test_update_recipes(self):
        recipes_id = self.recipes_api.generate_id_recipes()
        update_recipes = self.recipes_api.generate_update_recipes()
        with self.recipes_api.update_recipes(recipes_id, update_recipes) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Рецепт обновлён | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при обновлении рецепта | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(1)
    def test_delete_recipes(self):
        recipes_id = self.recipes_api.generate_id_recipes()
        with self.recipes_api.delete_recipes(recipes_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f"✅ Рецепт удалён | {response.status_code}")
            else:
                get_logger().error(f"❌ Ошибка при удалении рецепта | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")