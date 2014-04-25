import pytest


@pytest.fixture
def storage():
    from siilo.storages.base import Storage
    return Storage()


def test_delete_raises_not_implemented_error(storage):
    with pytest.raises(NotImplementedError):
        storage.delete('README.rst')


def test_exists_raises_not_implemented_error(storage):
    with pytest.raises(NotImplementedError):
        storage.exists('README.rst')


def test_open_raises_not_implemented_error(storage):
    with pytest.raises(NotImplementedError):
        storage.open('README.rst')


def test_size_raises_not_implemented_error(storage):
    with pytest.raises(NotImplementedError):
        storage.size('README.rst')


def test_url_raises_not_implemented_error(storage):
    with pytest.raises(NotImplementedError):
        storage.url('README.rst')
