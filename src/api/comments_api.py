from src.api.base_api import BaseAPI

class CommentsAPI(BaseAPI):
    """Класс отвечающий за эндпоинт /comments"""

    def get_comments(self, comment_id):
        return self.get(f"/comments/{comment_id}")

    def create_comments(self, comments_data: dict):
        return self.post(f"/comments/add", json=comments_data)

    def update_comments(self, comment_id, comments_data):
        return self.put(f"/comments/{comment_id}", json=comments_data)

    def delete_comments(self, comment_id):
        return self.delete(f"/comments/{comment_id}")