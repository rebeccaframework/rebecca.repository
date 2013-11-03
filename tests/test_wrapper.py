import pytest
from zope.interface.verify import verifyObject


class DummyAdapter(object):
    def __init__(self, item):
        self.item = item


class TestRepositoryWrapper(object):

    @pytest.fixture
    def target(self):
        from rebecca.repository.wrapper import RepositoryWrapper
        return RepositoryWrapper

    def test_iface(self, target):
        from rebecca.repository.interfaces import IRepository
        wrapper = target(None, None)

        verifyObject(IRepository, wrapper)

    def dummy_repository(self, dct):
        from uuid import uuid4
        from rebecca.repository.memory import OnMemoryRepository
        factory = lambda: dict(key=uuid4().hex)
        key = lambda item: item['key']
        return OnMemoryRepository(factory, key, dct)

    def test_getitem(self, target):

        wrapper = target(
            self.dummy_repository(
                {'testing': {'value': 'testing'}}),
            DummyAdapter)

        result = wrapper['testing']

        assert result.item == {'value': 'testing'}

    def test_get(self, target):
        wrapper = target(
            self.dummy_repository(
                {'testing': {'value': 'testing'}}),
            DummyAdapter)

        result = wrapper.get('testing')

        assert result.item == {'value': 'testing'}

    def test_get_none(self, target):
        wrapper = target(
            self.dummy_repository({}),
            DummyAdapter)

        result = wrapper.get('testing')

        assert result is None

    def test_get_many(self, target):
        wrapper = target(
            self.dummy_repository(
                {'testing': {'value': 'testing'},
                 'another': {'value': 'another', 'value2': 100}}),
            DummyAdapter)

        result = sorted(list(wrapper.get_many(['testing', 'another'])),
                        key=lambda item: item.item['value'])

        assert result[0].item == {'value': 'another', 'value2': 100}
        assert result[1].item == {'value': 'testing'}

    def test_new_item(self, target):
        wrapper = target(self.dummy_repository({}),
                         DummyAdapter)

        result = wrapper.new_item()

        assert result.item['key'] in wrapper.repository
