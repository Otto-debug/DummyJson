from src.api.base_api import BaseAPI

class TodosAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /todos/"""

    def get_todos(self, todos_id):
        return self.get(f'/todos/{todos_id}')

    def create_todos(self, todos_data: dict):
        return self.post(f'/todos/add', json=todos_data)

    def update_todos(self, todos_id, todos_data: dict):
        return self.put(f'/todos/{todos_id}', json=todos_data)

    def delete_todos(self, todos_id):
        return self.delete(f'/todos/{todos_id}')
