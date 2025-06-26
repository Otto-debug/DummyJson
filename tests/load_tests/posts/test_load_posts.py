import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.posts_api import PostsAPI
from utils.logger import get_logger

class TestLoadPosts(HttpUser):
    host = "https://dummyjson.com"

    def on_start(self) -> None:
        self.posts_api = PostsAPI(self.client)

    @task(15)
    def test_get_posts(self):
        with self.posts_api.get_posts() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /posts | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /posts | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(10)
    def test_create_posts(self):
        post_data = self.posts_api.generate_post()
        with self.posts_api.create_posts(post_data) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Пост создан | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при создании поста | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def test_update_posts(self):
        post_id = self.posts_api.generate_id_post()
        update_post = self.posts_api.generate_update_post()
        with self.posts_api.update_posts(post_id, update_post) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Пост обновлён | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при обновлении поста | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(1)
    def test_delete_post(self):
        post_id = self.posts_api.generate_id_post()
        with self.posts_api.delete_post(post_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f"✅ Пост удалён | {response.status_code}")
            else:
                get_logger().error(f"❌ Ошибка при удалении поста | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")
