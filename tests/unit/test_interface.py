import pytest


def get_storage_class():
    from silo.storages import Storage
    return Storage


def make_storage(*args, **kwargs):
    Storage = get_storage_class()
    return Storage(*args, **kwargs)


@pytest.mark.unit
class TestStorage(object):
    def test_accessed_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.accessed('README.rst')

    def test_created_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.created('README.rst')

    def test_delete_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.delete('README.rst')

    def test_exists_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.exists('README.rst')

    def test_list_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.list()

    def test_modified_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.modified('README.rst')

    def test_read_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.read('README.rst')

    def test_size_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.size('README.rst')

    def test_write_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.write('README.rst', 'This is a readme.')

    def test_url_raises_not_implemented_error(self):
        storage = make_storage()
        with pytest.raises(NotImplementedError):
            storage.url('README.rst')
