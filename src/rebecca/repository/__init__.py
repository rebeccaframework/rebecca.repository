from .config import includeme
from .interfaces import IRepository
from .decorators import repository_config


def get_repository(request, name):
    reg = request.registry
    return reg.queryUtility(IRepository, name=name)