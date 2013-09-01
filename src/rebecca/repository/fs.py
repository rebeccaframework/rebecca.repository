""" file system repository
"""

import os
from zope.interface import implementer
from .interfaces import IRepository


@implementer(IRepository)
class FileSystemRepository(object):
    def __init__(self, directory):
        self.directory = directory

    def __getitem__(self, key):
        filename = os.path.join(self.directory, key)
        if not os.path.exists(filename):
            raise KeyError()

        with open(filename, "rb") as f:
            return f.read()

    def get(self, key):
        filename = os.path.join(self.directory, key)
        if not os.path.exists(filename):
            return None

        with open(filename, "rb") as f:
            return f.read()

    def get_many(self, keys):
        for key in keys:
            yield self.get(key)

    def new_item(self):
        pass