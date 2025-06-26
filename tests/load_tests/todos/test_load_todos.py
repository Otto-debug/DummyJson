import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task
from src.load_api.todos_api import TodosAPI
from utils.logger import get_logger

class TestLoadTodos(HttpUser):
    host = 'https://dummyjson.com'

    def on_start(self) -> None:
        self.todos_api = TodosAPI(self.client)

    @task(15)
    def test_get_todos(self):
        with self.todos_api.get_todos() as response:
            if response.status_code == 200:
                get_logger().info(f"✅ Успешный запрос к /todos | Код: {response.status_code}")
            else:
                get_logger().error(f"❌Ошибка запроса /todos | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(10)
    def test_create_todos(self):
        todos_data = self.todos_api.generate_todos()
        with self.todos_api.create_todos(todos_data) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Задача создана | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при создании задачи | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(5)
    def test_update_todos(self):
        todos_id = self.todos_api.generate_id_todos()
        update_todos = self.todos_api.generate_update_todos()
        with self.todos_api.update_todos(todos_id, update_todos) as response:
            if response.status_code in [200, 201]:
                get_logger().info(f"✅ Задача обновлена | {response.json()}")
            else:
                get_logger().error(f"❌ Ошибка при обновлении задачи | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

    @task(1)
    def test_delete_todos(self):
        todos_id = self.todos_api.generate_id_todos()
        with self.todos_api.delete_todos(todos_id) as response:
            if response.status_code in [200, 204]:
                get_logger().info(f"✅ Задача удалена | {response.status_code}")
            else:
                get_logger().error(f"❌ Ошибка при удалении задачи | Код: {response.status_code}")
                response.failure(f"Ошибка: {response.status_code} | {response.text}")

