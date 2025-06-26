import random

from src.load_api.base_api import LocustBaseAPI

from mimesis import Text

text = Text()

class TodosAPI(LocustBaseAPI):

    def get_single_todo(self, todos_id):
        return self.get(f"/todos/{todos_id}", catch_response=True)

    def get_todos(self):
        return self.get(f"/todos", catch_response=True)

    def create_todos(self, todos_data):
        return self.post(f"/todos/add", json=todos_data, catch_response=True)

    def update_todos(self, todos_id, update_todos):
        return self.put(f"/todos/{todos_id}", json=update_todos, name='/todos/:id (PUT)', catch_response=True)

    def delete_todos(self, todos_id):
        return self.delete(f"/todos/{todos_id}", name='/todos/:id (DELETE)', catch_response=True)

    def generate_todos(self):
        return {
             'todo': text.text(quantity=5),
             'completed': True,
             'userId': random.randint(1, 207),
         }

    def generate_update_todos(self):
        return {
            'completed': random.choice([True, False])
        }

    def generate_id_todos(self):
        return random.randint(1, 253)