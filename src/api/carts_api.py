from src.api.base_api import BaseAPI

class CartsAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /carts"""

    def get_cart(self, cart_id):
        return self.get(f"/carts/{cart_id}")

    def create_cart(self, cart_data: dict):
        return self.post(f"/carts/add", json=cart_data)

    def update_cart(self, cart_id, cart_data: dict):
        return self.put(f"/carts/{cart_id}", json=cart_data)

    def delete_cart(self, cart_id):
        return self.delete(f"/cart/{cart_id}")
