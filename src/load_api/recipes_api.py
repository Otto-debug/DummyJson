import random

from src.load_api.base_api import LocustBaseAPI

from mimesis import Food

food = Food()

class RecipesAPI(LocustBaseAPI):

    def get_single_recipe(self, recipes_id):
        return self.get(f"/recipes/{recipes_id}", catch_response=True)

    def get_recipes(self):
        return self.get(f"/recipes", catch_response=True)

    def create_recipes(self, recipes_data):
        return self.post(f"/recipes/add", json=recipes_data, catch_response=True)

    def update_recipes(self, recipes_id, update_recipes):
        return self.put(f"/recipes/{recipes_id}", json=update_recipes, name='/recipes/:id (PUT)', catch_response=True)

    def delete_recipes(self, recipes_id):
        return self.delete(f"/recipes/{recipes_id}", name='/recipes/:id (DELETE)', catch_response=True)

    def generate_recipes(self):
        return {
            'name': food.drink()
        }

    def generate_update_recipes(self):
        return {
            'name': food.fruit()
        }

    def generate_id_recipes(self):
        return random.randint(1, 49)