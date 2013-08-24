from six import string_types
from sqlalchemy.orm.exc import NoResultFound
from zope.interface import implementer
from .interfaces import IRepository


@implementer(IRepository)
class SQLARepository(object):
    def __init__(self, model_cls, keyattr, dbsession, condition=None, orders=[]):
        self.model_cls = model_cls
        if isinstance(keyattr, string_types):
            self.keyattr = getattr(self.model_cls, keyattr)
        else:
            self.keyattr = keyattr
        self.dbsession = dbsession
        self.condition = condition
        self.orders = orders

    def new_item(self, *args, **kwargs):
        item = self.model_cls(*args, **kwargs)
        self.dbsession.add(item)
        return item

    def base_query(self):
        q = self.dbsession.query(
                self.model_cls
            )
        if self.condition is not None:
            q = q.filter(self.condition)
        return q

    def query(self, key):
        q = self.base_query()
        q = q.filter(
                self.keyattr==key
            )
        return q

    def iter_slice(self, s):
        q = self.base_query()
        return q[s.start:s.stop]

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.iter_slice(key)
        try:
            return self.query(key).one()
        except NoResultFound:
            raise KeyError(key)

    def get(self, key):
        return self.query(key).first()

    def __iter__(self):
        # TODO: support order
        return iter(self.base_query())

