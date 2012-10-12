from flexmock import flexmock


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


class TestStorage(object):

    def test_constructor_sets_adapter(self):
        adapter = flexmock()
        storage = make_storage(adapter)
        assert storage.adapter is adapter

    def test_contains_returns_false_if_key_doesnt_exist(self):
        storage = make_storage_with_fake_adapter()
        (
            storage.adapter
            .should_receive('exists')
            .with_args('README.rst')
            .and_return(False)
            .once()
        )
        assert 'README.rst' not in storage

    def test_contains_returns_true_if_key_exists(self):
        storage = make_storage_with_fake_adapter()
        (
            storage.adapter
            .should_receive('exists')
            .with_args('README.rst')
            .and_return(True)
            .once()
        )
        assert 'README.rst' in storage

    def test_getitem_returns_a_file_with_the_given_key(self):
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


class TestFile(object):
    def test_constructor_sets_storage(self):
        storage = flexmock()
        file_ = make_file(storage, 'README.rst')
        assert file_.storage is storage

    def test_constructor_sets_key(self):
        storage = flexmock()
        file_ = make_file(storage, 'README.rst')
        assert file_.key == 'README.rst'

    def test_exists_returns_false_if_key_doesnt_exist(self):
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

    def test_exists_returns_true_if_key_exists(self):
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
