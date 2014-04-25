import io
import os

import pytest

from siilo.exceptions import (
    FileNotAccessibleViaURLError,
    FileNotFoundError,
    FileNotWithinStorageError,
)


@pytest.fixture
def storage(tmpdir):
    from siilo.storages.filesystem import FileSystemStorage
    return FileSystemStorage(
        base_directory=str(tmpdir),
        base_url='http://www.example.com/'
    )


def test_storage_repr(storage):
    expected = '<FileSystemStorage base_directory={0!r}>'.format(
        storage.base_directory
    )
    assert repr(storage) == expected


def test_constructor_sets_base_directory(storage, tmpdir):
    assert storage.base_directory == str(tmpdir)


def test_constructor_sets_base_url(storage):
    assert storage.base_url == 'http://www.example.com/'


def test_relative_base_directory_is_normalized(storage):
    storage.base_directory = 'foobar'
    assert storage.base_directory == os.path.abspath('foobar')


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


@pytest.mark.parametrize(
    'mode',
    ['a', 'a+', 'ab', 'ab+', 'w', 'w+', 'wb', 'wb+']
)
def test_open_makes_path_if_it_doesnt_exist(storage, tmpdir, mode):
    path = tmpdir.join('some', 'dir')
    filename = str(path.join('foobar'))
    file_ = storage.open(filename, mode)
    assert path.exists()
    assert file_.name == filename


@pytest.mark.parametrize(
    'mode',
    ['r', 'r+', 'rb', 'r+b']
)
def test_open_doesnt_make_path_for_read_modes(storage, tmpdir, mode):
    path = tmpdir.join('some', 'dir')
    filename = str(path.join('foobar'))
    with pytest.raises(FileNotFoundError):
        storage.open(filename, mode)
    assert not path.exists()


@pytest.mark.parametrize(
    ('name', 'url'),
    [
        ('file.txt', 'http://www.example.com/file.txt'),
        ('dir/file.txt', 'http://www.example.com/dir/file.txt'),
        ('file name.txt', 'http://www.example.com/file%20name.txt'),
    ]
)
def test_url_returns_url_to_the_file(storage, name, url):
    assert storage.url(name) == url


def test_url_raises_error_if_base_url_not_set(storage):
    storage.base_url = None
    with pytest.raises(FileNotAccessibleViaURLError) as excinfo:
        storage.url('file.txt')
    assert excinfo.value.name == 'file.txt'
