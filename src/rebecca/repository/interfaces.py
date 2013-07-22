from zope.interface import Interface


class IRepository(Interface):

    def __getitem__(key):
        """ get item from repository"""
