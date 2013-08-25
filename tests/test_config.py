import pytest
from pyramid import testing

class TestIncludeMe(object):

    @pytest.fixture
    def config(self, request):
        config = testing.setUp()
        def fin():
            testing.tearDown()
        request.addfinalizer(fin)
        return config

    @pytest.fixture
    def target(self):
        from rebecca.repository.config import includeme
        return includeme

    def test_it(self, target, config):
        target(config)

        assert hasattr(config, 'add_repository')

class TestAddRepository(object):

    @pytest.fixture
    def config(self, request):
        config = testing.setUp()
        def fin():
            testing.tearDown()
        request.addfinalizer(fin)
        return config

    @pytest.fixture
    def target(self):
        from rebecca.repository.config import add_repository
        return add_repository

    def test_it(self, target, config):
        from rebecca.repository.interfaces import IRepository
        repository1 = testing.DummyResource()
        target(config, repository1, "testing1")
        repository2 = testing.DummyResource()
        target(config, repository2, "testing2")

        registered = config.registry.getUtility(IRepository, name="testing1")

        assert registered == repository1

        intr = config.registry.introspector.get('rebecca.repository', 'testing1')

        assert intr['value'] == repository1
        assert intr.title == 'rebecca.repository:testing1'