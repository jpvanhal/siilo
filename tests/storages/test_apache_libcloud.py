# -*- coding: utf-8 -*-
import locale
import os
try:
    from unittest import mock
except ImportError:
    import mock

from libcloud.storage.base import Container
from libcloud.storage.types import ObjectDoesNotExistError
import pytest

from siilo.exceptions import FileNotFoundError


@pytest.fixture
def container():
    return mock.MagicMock(name='container', spec=Container)


@pytest.fixture
def storage(container):
    from siilo.storages.apache_libcloud import ApacheLibcloudStorage
    return ApacheLibcloudStorage(container=container)


@pytest.fixture
def object_does_not_exist():
    return ObjectDoesNotExistError(
        driver=mock.sentinel.driver,
        value=mock.sentinel.value,
        object_name=mock.sentinel.object_name
    )


def test_storage_repr(storage, container):
    expected = '<ApacheLibcloudStorage container={0!r}>'.format(container)
    assert repr(storage) == expected


def test_delete_removes_the_file(storage, container):
    storage.delete('some_file.txt')
    container.get_object.assert_called_with('some_file.txt')
    obj = container.get_object('some_file.txt')
    assert obj.delete.called


def test_delete_raises_error_if_file_doesnt_exist_on_get_object(
    storage, container, object_does_not_exist
):
    container.get_object.side_effect = object_does_not_exist
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.delete('some_file.txt')
    assert excinfo.value.name == 'some_file.txt'


def test_delete_raises_error_if_file_doesnt_exist_on_delete(
    storage, container, object_does_not_exist
):
    obj = container.get_object('some_file.txt')
    obj.delete.side_effect = object_does_not_exist
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.delete('some_file.txt')
    assert excinfo.value.name == 'some_file.txt'


def test_exists_returns_false_if_file_doesnt_exist(
    storage, container, object_does_not_exist
):
    container.get_object.side_effect = object_does_not_exist
    assert storage.exists('some_file.txt') is False


def test_exists_returns_true_if_file_exists(storage, container):
    assert storage.exists('some_file.txt') is True
    container.get_object.assert_called_with('some_file.txt')


def test_size_returns_file_size_in_bytes(storage, container):
    obj = container.get_object('some_file.txt')
    assert storage.size('some_file.txt') == obj.size


def test_size_raises_error_if_file_doesnt_exist(
    storage, container, object_does_not_exist
):
    container.get_object.side_effect = object_does_not_exist
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.size('some_file.txt')
    assert excinfo.value.name == 'some_file.txt'


def test_url_returns_files_url(storage, container):
    obj = container.get_object('some_file.txt')
    assert storage.url('some_file.txt') == obj.get_cdn_url()


def test_url_raises_error_if_file_doesnt_exist(
    storage, container, object_does_not_exist
):
    container.get_object.side_effect = object_does_not_exist
    with pytest.raises(FileNotFoundError) as excinfo:
        storage.url('some_file.txt')
    assert excinfo.value.name == 'some_file.txt'


def test_open_returns_libcloud_file_with_default_mode_and_encoding(storage):
    with mock.patch(
        'siilo.storages.apache_libcloud.LibcloudFile'
    ) as MockLibcloudFile:
        MockLibcloudFile.return_value = mock.sentinel.file
        file_ = storage.open('some_file.txt')
        MockLibcloudFile.assert_called_with(
            storage=storage,
            name='some_file.txt',
            mode='r',
            encoding=None
        )
        assert file_ is mock.sentinel.file


def test_open_returns_libcloud_file_with_given_mode_and_encoding(storage):
    with mock.patch(
        'siilo.storages.apache_libcloud.LibcloudFile'
    ) as MockLibcloudFile:
        MockLibcloudFile.return_value = mock.sentinel.file
        file_ = storage.open('some_file.txt', 'w', 'utf-8')
        MockLibcloudFile.assert_called_with(
            storage=storage,
            name='some_file.txt',
            mode='w',
            encoding='utf-8'
        )
        assert file_ is mock.sentinel.file


@pytest.mark.parametrize(
    'mode', ['a', 'a+', 'a+b', 'ab', 'r', 'r+', 'r+b', 'rb']
)
def test_downloads_file_for_read_and_append_modes(storage, container, mode):
    contents = b'Quick brown fox jumps over lazy dog'

    obj = container.get_object('some_file.txt')
    obj.as_stream.return_value = iter([contents])

    with storage.open('some_file.txt', mode) as file_:
        with open(file_._temporary_filename, 'rb') as tempfile:
            assert tempfile.read() == contents


@pytest.mark.parametrize('mode', ['w', 'wb', 'w+', 'w+b'])
def test_doesnt_download_file_for_write_modes(storage, container, mode):
    with storage.open('some_file.txt', mode):
        pass

    assert not container.get_object.called


@pytest.mark.parametrize(
    ('mode', 'encoding'),
    [
        ('r', None),
        ('w', 'UTF-8'),
    ]
)
def test_opens_temporary_file_with_given_mode_and_encoding(
    storage, mode, encoding
):
    with storage.open('some_file.txt', mode, encoding) as file_:
        assert file_._stream.name == file_._temporary_filename
        assert file_._stream.mode == mode
        assert file_._stream.encoding == encoding or locale.getdefaultlocale()


@pytest.mark.parametrize(
    'filename',
    [
        '/etc/passwd',
        '../etc/passwd',
    ]
)
def test_always_opens_temporary_file_within_the_temporary_directory(
    storage, filename
):
    with storage.open(filename) as file_:
        assert file_._temporary_filename == os.path.abspath(
            file_._temporary_filename
        )
        assert file_._temporary_filename.startswith(file_._temporary_directory)


@pytest.mark.parametrize(
    'mode',
    ['a', 'a+', 'a+b', 'ab', 'w', 'wb', 'w+', 'w+b']
)
def test_uploads_file_opened_in_write_mode_but_not_written_to_to_storage(
    storage, container, mode, object_does_not_exist
):
    container.get_object.side_effect = object_does_not_exist
    with mock.patch('siilo.storages.apache_libcloud.io.open') as mock_open:
        mock_open.return_value = mock.MagicMock(closed=False)
        with storage.open('some_file.txt', mode) as file_:
            pass
    with mock_open(file_._temporary_filename, mode='rb') as temp_file:
        container.upload_object_via_stream.assert_called_with(
            iterator=temp_file,
            object_name='some_file.txt'
        )


@pytest.mark.parametrize(
    'mode',
    ['a', 'a+', 'a+b', 'ab', 'r+', 'r+b', 'w', 'wb', 'w+', 'w+b']
)
@pytest.mark.parametrize(
    ('method_name', 'method_args'),
    [
        ('write', 'foo'),
        ('writelines', ['foo', 'bar']),
    ]
)
def test_uploads_file_written_to_to_storage(
    storage, container, mode, method_name, method_args
):
    with mock.patch('siilo.storages.apache_libcloud.io.open') as mock_open:
        mock_open.return_value = mock.MagicMock(closed=False)
        with storage.open('some_file.txt', mode) as file_:
            method = getattr(file_, method_name)
            method(method_args)
    with mock_open(file_._temporary_filename, mode='rb') as temp_file:
        container.upload_object_via_stream.assert_called_with(
            iterator=temp_file,
            object_name='some_file.txt'
        )


@pytest.mark.parametrize(
    'mode',
    ['a', 'a+', 'a+b', 'ab', 'r', 'rb', 'r+', 'r+b']
)
def test_doesnt_upload_file_if_file_not_written_to(storage, container, mode):
    with storage.open('some_file.txt', mode):
        pass
    assert not container.upload_object_via_stream.called


def test_removes_temporary_directory_after_file_is_closed(storage, container):
    with storage.open('some_file.txt', 'r') as file_:
        pass
    assert not os.path.exists(file_._temporary_directory)


@pytest.mark.parametrize(
    ('method_name', 'method_args', 'method_returns'),
    [
        ('fileno', [], True),
        ('flush', [], False),
        ('isatty', [], True),
        ('read', [], True),
        ('readable', [], True),
        ('readall', [], True),
        ('readinto', [], True),
        ('readline', [], True),
        ('readlines', [], True),
        ('seekable', [], True),
        ('tell', [], False),
        ('writable', [], True),
        ('write', ['foo'], False),
        ('writelines', [['foo', 'bar']], False),
    ]
)
def test_delegates_file_api_methods_to_underlying_temporary_file(
    storage, method_name, method_args, method_returns
):
    with storage.open('some_file.txt', 'r') as file_:
        file_._stream = mock.MagicMock(name='stream')

        method = getattr(file_, method_name)
        rv = method(*method_args)

    stream_method = getattr(file_._stream, method_name)
    stream_method.assert_called_with(*method_args)
    if method_returns:
        assert rv == stream_method(*method_args)


@pytest.mark.parametrize(
    'property_name',
    [
        'closed',
        'encoding',
        'mode',
    ]
)
def test_delegates_file_api_properties_to_underlying_temporary_file(
    storage, property_name
):
    with storage.open('some_file.txt', 'r') as file_:
        file_._stream = mock.MagicMock(name='stream')

        actual_value = getattr(file_, property_name)
        expected_value = getattr(file_._stream, property_name)

    assert actual_value == expected_value


def test_reclosing_file_is_noop(storage):
    with storage.open('some_file.txt', 'r') as file_:
        pass
    file_.close()


def test_can_iterate_over_file(storage, container):
    contents = b'Quick brown fox\njumps over lazy dog'

    obj = container.get_object('some_file.txt')
    obj.as_stream.return_value = iter([contents])

    with storage.open('some_file.txt', 'r') as file_:
        lines = list(line for line in file_)

    assert lines == [
        u'Quick brown fox\n',
        u'jumps over lazy dog',
    ]


@pytest.mark.parametrize(
    ('mode', 'encoding', 'expected_format'),
    [
        (
            'r',
            'UTF-8',
            (
                '<LibcloudFile storage={storage!r}, name={name!r}, '
                'mode={mode!r}, encoding={encoding!r}>'
            )
        ),
        (
            'rb',
            None,
            '<LibcloudFile storage={storage!r}, name={name!r}, mode={mode!r}>'
        ),
    ]
)
def test_libcloudfile_repr(storage, mode, encoding, expected_format):
    with storage.open('some_file.txt', mode, encoding) as file_:
        assert repr(file_) == expected_format.format(
            storage=storage,
            name=file_.name,
            mode=file_.mode,
            encoding=encoding
        )
