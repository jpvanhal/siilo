from datetime import datetime

from flexmock import flexmock
import pytest


def get_storage_class():
    from unistorage.core import Storage
    return Storage


def get_file_class():
    from unistorage.core import File
    return File


def make_storage(*args, **kwargs):
    Storage = get_storage_class()
    return Storage(*args, **kwargs)


def make_file(*args, **kwargs):
    File = get_file_class()
    return File(*args, **kwargs)


def make_storage_with_fake_adapter():
    adapter = flexmock()
    storage = make_storage(adapter)
    return storage


@pytest.mark.unit
class TestStorage(object):

    def test_constructor_sets_adapter(self):
        adapter = flexmock()
        storage = make_storage(adapter)
        assert storage.adapter is adapter

    def test_contains_returns_false_if_file_doesnt_exist(self):
        storage = make_storage_with_fake_adapter()
        (
            storage.adapter
            .should_receive('exists')
            .with_args('README.rst')
            .and_return(False)
            .once()
        )
        assert 'README.rst' not in storage

    def test_contains_returns_true_if_file_exists(self):
        storage = make_storage_with_fake_adapter()
        (
            storage.adapter
            .should_receive('exists')
            .with_args('README.rst')
            .and_return(True)
            .once()
        )
        assert 'README.rst' in storage

    def test_getitem_returns_a_file_with_the_given_name(self):
        from unistorage import core
        storage = make_storage_with_fake_adapter()
        fake_file = flexmock()
        (
            flexmock(core)
            .should_receive('File')
            .with_args(storage, 'README.rst')
            .and_return(fake_file)
            .once()
        )
        assert storage['README.rst'] is fake_file


@pytest.mark.unit
class TestFile(object):
    def test_constructor_sets_storage(self):
        storage = flexmock()
        file_ = make_file(storage, 'README.rst')
        assert file_.storage is storage

    def test_constructor_sets_filename(self):
        storage = flexmock()
        file_ = make_file(storage, 'README.rst')
        assert file_.name == 'README.rst'

    def test_exists_returns_false_if_file_doesnt_exist(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage)
            .should_receive('__contains__')
            .with_args('README.rst')
            .and_return(False)
            .once()
        )
        assert not file_.exists

    def test_exists_returns_true_if_file_exists(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage)
            .should_receive('__contains__')
            .with_args('README.rst')
            .and_return(True)
            .once()
        )
        assert file_.exists

    def test_size_returns_file_size(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('size')
            .with_args('README.rst')
            .and_return(42)
            .once()
        )
        assert file_.size == 42

    def test_getting_content_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('read')
            .with_args('README.rst')
            .and_return('This is a readme.')
            .once()
        )
        assert file_.content == 'This is a readme.'

    def test_setting_content_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('write')
            .with_args('README.rst', 'This is a readme.')
            .once()
        )
        file_.content = 'This is a readme.'

    def test_url_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('url')
            .with_args('README.rst')
            .and_return('http://static.example.com/README.rst')
            .once()
        )
        assert file_.url == 'http://static.example.com/README.rst'

    def test_delete_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('delete')
            .with_args('README.rst')
            .once()
        )
        file_.delete()

    def test_accessed_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        accessed = datetime.utcnow()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('accessed')
            .with_args('README.rst')
            .and_return(accessed)
            .once()
        )
        assert file_.accessed is accessed

    def test_created_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        created = datetime.utcnow()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('created')
            .with_args('README.rst')
            .and_return(created)
            .once()
        )
        assert file_.created is created

    def test_modified_delegates_to_adapter(self):
        storage = make_storage_with_fake_adapter()
        modified = datetime.utcnow()
        file_ = make_file(storage, 'README.rst')
        (
            flexmock(storage.adapter)
            .should_receive('modified')
            .with_args('README.rst')
            .and_return(modified)
            .once()
        )
        assert file_.modified is modified
