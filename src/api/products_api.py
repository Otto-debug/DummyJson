from src.api.base_api import BaseAPI

class ProductsAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /products"""

    def get_product(self, product_id):
        return self.get(f"/products/{product_id}")

    def create_product(self, product_data: dict):
        return self.post(f"/product/add", json=product_data)

    def update_product(self, product_id, product_data: dict):
        return self.put(f"/products/{product_id}", json=product_data)

    def delete_product(self, product_id):
        return self.delete(f"/products/{product_id}")
