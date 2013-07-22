from zope.interface import implementer
from sqlalchemy.orm.exc import NoResultFound
from .interfaces import IRepository

@implementer(IRepository)
class SQLARepository(object):
    def __init__(self, model_cls, keyattr, dbsession):
        self.model_cls = model_cls
        self.keyattr = keyattr
        self.dbsession = dbsession

    def __getitem__(self, key):
        try:
            return self.dbsession.query(
                self.model_cls
            ).filter(
                getattr(self.model_cls, self.keyattr)==key
            ).one()
        except NoResultFound:
            raise KeyError(key)
