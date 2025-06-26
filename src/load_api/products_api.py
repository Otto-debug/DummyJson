import random

from src.load_api.base_api import LocustBaseAPI

from mimesis import Hardware

hardware = Hardware()

class ProductsAPI(LocustBaseAPI):

    def get_single_product(self, product_id):
        return self.get(f"/products/{product_id}", catch_response=True)

    def get_products(self):
        return self.get(f"/products/", catch_response=True)

    def create_products(self, product_data):
        return self.post(f"/products/add", json=product_data, catch_response=True)

    def updt_product(self, product_id, update_data):
        return self.put(f'/products/{product_id}', json=update_data, name='/products/:id (PUT)', catch_response=True)

    def delete_products(self, product_id):
        return self.delete(f"/products/{product_id}", name='/products/:id', catch_response=True)

    def generate_fake_product(self):
        return {
            "title": hardware.cpu()
        }

    def generate_update_product(self):
        return {
            "title": hardware.phone_model()
        }

    def generate_random_product_id(self):
        return random.randint(1, 194)