from zope.interface import Interface


class IRepository(Interface):

    def __getitem__(key):
        """ get item from repository"""

    def get(key):
        """ get item safely
        """

    def new_item():
        """ new item within repository
        """