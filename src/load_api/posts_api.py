import random

from src.load_api.base_api import LocustBaseAPI

from mimesis import Text, Person
from mimesis.enums import Gender

text = Text()
person = Person()


class PostsAPI(LocustBaseAPI):

    def get_single_post(self, post_id):
        return self.get(f"/posts/{post_id}", catch_response=True)

    def get_posts(self):
        return self.get(f"/posts/", catch_response=True)

    def create_posts(self, post_data):
        return self.post(f"/posts/add", json=post_data, catch_response=True)

    def update_posts(self, post_id, update_post):
        return self.put(f"/posts/{post_id}", json=update_post, name="/posts/:id (PUT)", catch_response=True)

    def delete_post(self, post_id):
        return self.delete(f"/posts/{post_id}", name="/posts/:id (DELETE)", catch_response=True)

    def generate_post(self):
        return {
            "title": text.title(),
            "body": text.text(quantity=1),
            "userId": random.randint(1, 100),
            "tags": [text.word() for _ in range(3)]
        }

    def generate_update_post(self):
        return {"title": text.title(), "body": text.text(quantity=2)}

    def generate_id_post(self):
        return random.randint(1, 250)