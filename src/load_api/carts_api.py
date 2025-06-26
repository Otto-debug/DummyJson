from src.load_api.base_api import LocustBaseAPI

import random
from mimesis import Hardware

class CartsAPI(LocustBaseAPI):

    def get_single_cart(self, cart_id):
        return self.get(f"/carts/{cart_id}", catch_response=True)

    def get_carts(self):
        return self.get(f"/carts", catch_response=True)

    def create_cart(self, cart_data):
        return self.post(f"/carts/add", json=cart_data, catch_response=True)

    def update_cart(self, cart_id, update_cart):
        return self.put(f"/carts/{cart_id}", json=update_cart, name='/carts/:id (PUT)', catch_response=True)

    def delete_carts(self, cart_id):
        return self.delete(f"/carts/{cart_id}", name='/users/:id (DELETE)', catch_response=True)

    def generate_cart(self):
        return {
            'userId': random.randint(1, 50),
            'products': [
                {
                    'id': random.randint(1, 144),
                    'quantity': random.randint(1, 10)
                },
                {
                    'id': random.randint(1, 144),
                    'quantity': random.randint(1, 10)
                }
            ]
        }

    def generate_update_cart(self):
        return {
            'products': [
                {
                    'id': random.randint(1, 144),
                    'quantity': random.randint(1, 10)
                }
            ]
        }

    def generate_cart_id(self):
        return random.randint(1, 50)