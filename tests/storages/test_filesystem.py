import io
import os

import pytest

from silo.exceptions import FileNotFoundError, FileNotWithinStorageError


@pytest.fixture
def storage(tmpdir):
    from silo.storages.filesystem import FileSystemStorage
    return FileSystemStorage(directory=str(tmpdir))


def test_constructor_sets_directory(storage, tmpdir):
    assert storage.directory == str(tmpdir)


def test_relative_directory_is_normalized(storage):
    storage.directory = 'foobar'
    assert storage.directory == os.path.abspath('foobar')


def test_delete_removes_the_file(storage, tmpdir):
    file_ = tmpdir.join('foobar').ensure()
    storage.delete('foobar')
    assert not file_.check()


def test_delete_raises_error_if_file_doesnt_exist(storage):
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.delete('foobar')
    assert excinfo.value.name == 'foobar'


def test_delete_raises_error_if_file_not_within_storage(storage):
    with pytest.raises(FileNotWithinStorageError) as excinfo:
        storage.delete('../foobar')
    assert excinfo.value.name == '../foobar'


def test_exists_returns_false_if_file_doesnt_exist(storage):
    assert storage.exists('foobar') is False


def test_exists_returns_true_if_file_exists(storage, tmpdir):
    tmpdir.join('foobar').ensure()
    assert storage.exists('foobar') is True


def test_exists_raises_error_if_file_not_within_storage(storage):
    with pytest.raises(FileNotWithinStorageError) as excinfo:
        storage.exists('../foobar')
    assert excinfo.value.name == '../foobar'


def test_size_returns_file_size_in_bytes(storage, tmpdir):
    tmpdir.join('foobar').write('xyzzy')
    assert storage.size('foobar') == 5


def test_size_raises_error_if_file_doesnt_exist(storage):
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.size('foobar')
    assert excinfo.value.name == 'foobar'


def test_size_raises_error_if_file_not_within_storage(storage):
    with pytest.raises(FileNotWithinStorageError) as excinfo:
        storage.size('../foobar')
    assert excinfo.value.name == '../foobar'


def test_open_returns_open_file_with_default_mode(storage, tmpdir):
    tmpdir.join('foobar').ensure()
    file_ = storage.open('foobar')
    assert isinstance(file_, io.IOBase)
    assert file_.name == str(tmpdir.join('foobar'))
    assert file_.mode == 'rb'


def test_open_returns_open_file_with_given_mode(storage, tmpdir):
    file_ = storage.open('foobar', 'w')
    assert isinstance(file_, io.IOBase)
    assert file_.name == str(tmpdir.join('foobar'))
    assert file_.mode == 'w'


def test_open_raises_error_if_file_doesnt_exist(storage):
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.open('foobar', 'r')
    assert excinfo.value.name == 'foobar'


def test_open_raises_error_if_file_not_within_storage(storage):
    with pytest.raises(FileNotWithinStorageError) as excinfo:
        storage.open('../foobar')
    assert excinfo.value.name == '../foobar'
