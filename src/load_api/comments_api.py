import random

from src.load_api.base_api import LocustBaseAPI

from mimesis import Text

text = Text()

class CommentsAPI(LocustBaseAPI):

    def get_single_comment(self, comment_id):
        return self.get(f"/comments/{comment_id}", catch_response=True)

    def get_comments(self):
        return self.get(f"/comments/", catch_response=True)

    def create_comments(self, comment_data):
        return self.post(f"/comments/add", json=comment_data, catch_response=True)

    def update_comments(self, comment_id, update_comment):
        return self.put(f"/comments/{comment_id}", json=update_comment, name="/comments/:id (PUT)", catch_response=True)

    def delete_comment(self, comment_id):
        return self.delete(f"/comments/{comment_id}", name="/comments/:id (DELETE)", catch_response=True)

    def generate_comment(self):
        return {
             'body': text.text(quantity=5),
             'postId': random.randint(1, 10),
             'userId': random.randint(1, 207),
         }

    def generate_update_comment(self):
        return {'body': text.text(quantity=2)}

    def generate_id_comment(self):
        return random.randint(1, 250)