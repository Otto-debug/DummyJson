from src.api.base_api import BaseAPI

class PostsAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /posts/"""

    def get_post(self, post_id):
        return self.get(f'/posts/{post_id}')

    def create_post(self, post_data: dict):
        return self.post(f'/posts/add', json=post_data)

    def update_post(self, post_id, post_data: dict):
        return self.put(f'/posts/{post_id}', json=post_data)

    def delete_post(self, post_id):
        return self.delete(f'/posts/{post_id}')
