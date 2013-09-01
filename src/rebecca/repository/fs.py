""" file system repository
"""

import os
from zope.interface import implementer
from repoze.filesafe import open_file
from .interfaces import IRepository


class Item(object):
    def __init__(self, key, data, repository):
        self.key = key
        self.repository = repository
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self.repository._write(self.key, value)
        self._data = value

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
        return Item(key, data, self)

    def _write(self, key, data):
        filename = os.path.join(self.directory, key)

        with open_file(filename, "wb") as f:
            return f.write(data)
