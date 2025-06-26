import random
from faker import Faker

from src.load_api.base_api import LocustBaseAPI

faker = Faker()

class UsersAPI(LocustBaseAPI):
    def get_all_users(self):
        return self.get("/users", catch_response=True)

    def get_user_by_id(self, user_id):
        return self.get(f"/users/{user_id}", catch_response=True)

    def create_user(self, user_data):
        return self.post(f"/users/add", json=user_data, catch_response=True)

    def updt_user(self, user_id, user_data):
        return self.put(f"/users/{user_id}", json=user_data, name="/users/:id (PUT)", catch_response=True)

    def delete_user(self, user_id):
        return self.delete(f"/users/{user_id}",  name="/users/:id (DELETE)", catch_response=True)

    def generate_fake_user(self):
        random_id = random.randint(1000, 99999)
        return {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "age": random.randint(18, 65),
            "email": faker.email()
        }

    def generate_user_update(self):
        return {
            "firstName": faker.first_name(),
            "lastName": faker.last_name()
        }

    def generate_id_user(self):
        return random.randint(1, 208)
