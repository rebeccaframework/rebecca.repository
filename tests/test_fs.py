import pytest
from testfixtures import TempDirectory, ShouldRaise

@pytest.fixture
def tempdir(request):
    d = TempDirectory()

    def fin():
        d.cleanup()
    request.addfinalizer(fin)
    return d

class TestFileSystemRepository(object):

    @pytest.fixture
    def target(self):
        from rebecca.repository.fs import FileSystemRepository
        return FileSystemRepository

    def test_get_item(self, target, tempdir):
        repository = target(tempdir.path)
        tempdir.write('test.txt', b'abcde')

        result = repository['test.txt']

        assert result == b'abcde'

    def test_get_item_key_error(self, target, tempdir):
        repository = target(tempdir.path)

        with ShouldRaise(KeyError):
            repository['test.txt']

    def test_get(self, target, tempdir):
        repository = target(tempdir.path)
        tempdir.write('test.txt', b'abcde')

        result = repository.get('test.txt')

        assert result == b'abcde'

    def test_get_key_error(self, target, tempdir):
        repository = target(tempdir.path)

        result = repository.get('test.txt')

        assert result is None

    def test_get_many(self, target, tempdir):
        repository = target(tempdir.path)
        tempdir.write('test1.txt', b'abcde')
        tempdir.write('test2.txt', b'fghi')

        result = list(repository.get_many(['test1.txt', 'test2.txt']))

        assert result == [b'abcde', b'fghi']

    def test_new_item(self, target, tempdir):
        repository = target(tempdir.path)

        item = repository.new_item('testing', b'aaaaaaaaa')

        assert item.key == "testing"
        assert item.data == b"aaaaaaaaa"
        assert tempdir.read('testing') == b'aaaaaaaaa'
