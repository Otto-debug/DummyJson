class LocustBaseAPI:
    def __init__(self, client):
        self.client = client

    def get(self, endpoint, **kwargs):
        return self.client.get(endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.client.post(endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.client.put(endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.client.delete(endpoint, **kwargs)
