class FakeRedis:
    def __init__(self):
        self.store = {}

    async def set(self, key, value):
        self.store[key] = value

    async def get(self, key):
        return self.store.get(key)