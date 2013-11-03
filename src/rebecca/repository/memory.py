class OnMemoryRepository(dict):
    def __init__(self, factory, keyfunc, dct={}):
        super(OnMemoryRepository, self).__init__()
        self.update(dct)
        self.factory = factory
        self.keyfunc = keyfunc

    def get_many(self, keys):
        return (value for key, value in self.items() if key in keys)

    def new_item(self):
        item = self.factory()
        key = self.keyfunc(item)
        self[key] = item
        return item
