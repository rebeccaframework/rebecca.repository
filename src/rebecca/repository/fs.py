""" file system repository
"""

import os
from zope.interface import implementer
from repoze.filesafe import open_file
from .interfaces import IRepository


class Item(object):
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def __enter__(self):
        self.f = open(self.filename, "wb")
        self.f.write(self.data)
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()

@implementer(IRepository)
class FileSystemRepository(object):
    def __init__(self, directory):
        self.directory = directory

    def __getitem__(self, key):
        filename = os.path.join(self.directory, key)
        if not os.path.exists(filename):
            raise KeyError()

        with open_file(filename, "rb") as f:
            return f.read()

    def get(self, key):
        filename = os.path.join(self.directory, key)
        if not os.path.exists(filename):
            return None

        with open_file(filename, "rb") as f:
            return f.read()

    def get_many(self, keys):
        for key in keys:
            yield self.get(key)

    def new_item(self, key, data):
        return Item(os.path.join(self.directory, key), data)
