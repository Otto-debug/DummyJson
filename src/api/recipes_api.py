from src.api.base_api import BaseAPI

class RecipesAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /recipes"""

    def get_recipes(self, recipes_id):
        return self.get(f"/recipes/{recipes_id}")

    def create_recipes(self, recipes_data: dict):
        return self.post(f"/recipes/add", json=recipes_data)

    def update_recipes(self, recipes_id, recipes_data: dict):
        return self.put(f"/recipes/{recipes_id}", json=recipes_data)

    def delete_recipes(self, recipes_id):
        return self.delete(f"/recipes/{recipes_id}")