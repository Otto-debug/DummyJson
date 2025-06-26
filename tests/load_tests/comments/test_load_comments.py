import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.comments_api import CommentsAPI
from utils.logger import get_logger

class TestLoadComments(HttpUser):
    host = 'https://dummyjson.com'

    def on_start(self) -> None:
        self.comments_api = CommentsAPI(self.client)

    @task(15)
    def test_get_comments(self):
        with self.comments_api.get_comments() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /comments | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /comments | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(10)
    def test_create_comments(self):
        comment_data = self.comments_api.generate_comment()
        with self.comments_api.create_comments(comment_data) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Комментарий создан | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при создании комментария | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def test_update_comments(self):
        comment_id = self.comments_api.generate_id_comment()
        update_comment = self.comments_api.generate_update_comment()
        with self.comments_api.update_comments(comment_id, update_comment) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Комментарий обновлён | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при обновлении комментария | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(1)
    def test_delete_comment(self):
        comment_id = self.comments_api.generate_id_comment()
        with self.comments_api.delete_comment(comment_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f"✅ Комментарий удалён | {response.status_code}")
            else:
                get_logger().error(f"❌ Ошибка при удалении комментария | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

