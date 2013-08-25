from pyramid import testing
from pyramid.config import Configurator
from rebecca.repository import repository_config
from rebecca.repository import get_repository


def test_app():
    conf = Configurator()
    conf.include('rebecca.repository')
    conf.scan(".")
    conf.commit()
    request = testing.DummyResource(registry=conf.registry)
    result = get_repository(request, "testing")

    assert isinstance(result, TestingRepository)
    assert result.value == 9999

@repository_config(name="testing", args=(9999,))
class TestingRepository(object):
    """ testing
    """

    def __init__(self, value):
        self.value = value