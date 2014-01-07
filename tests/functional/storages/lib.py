import datetime
import types

import pytest

from silo.exceptions import FileNotFound


@pytest.mark.functional
class FunctionalTestCase(object):
    def make_storage(self):
        raise NotImplementedError

    def teardown_storage(self, storage):
        pass

    def setup_method(self, method):
        self.storage = self.make_storage()

    def teardown_method(self, method):
        if hasattr(self, 'storage'):
            self.teardown_storage(self.storage)

    def test_read_fails_when_reading_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            self.storage.read('README.rst')
            assert exc.name == 'README.rst'

    def test_writing_and_reading(self):
        self.storage.write('README.rst', 'This is a readme.')
        content = self.storage.read('README.rst')
        assert content == 'This is a readme.'

    def test_write_updates_existing_file(self):
        self.storage.write('README.rst', 'This is a readme.')
        self.storage.write('README.rst', 'This is an updated readme.')
        content = self.storage.read('README.rst')
        assert content == 'This is an updated readme.'

    def test_checking_file_existence(self):
        assert not self.storage.exists('README.rst')
        self.storage.write('README.rst', 'This is a readme.')
        assert self.storage.exists('README.rst')

    def test_writing_and_deleting(self):
        self.storage.write('README.rst', 'This is a readme.')
        assert self.storage.exists('README.rst')
        self.storage.delete('README.rst')
        assert not self.storage.exists('README.rst')

    def test_delete_does_not_fail_when_deleting_non_existing_file(self):
        self.storage.delete('README.rst')

    def test_size_returns_file_size(self):
        self.storage.write('README.rst', 'This is a readme.')
        assert self.storage.size('README.rst') == 17

    def test_size_fails_when_accessing_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            self.storage.size('README.rst')
            assert exc.name == 'README.rst'

    def test_modified_fails_when_accessing_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            try:
                self.storage.modified('README.rst')
                assert exc.name == 'README.rst'
            except NotImplementedError:
                pytest.skip("not implemented in this storage")

    def test_modified_returns_files_modified_time(self):
        now = datetime.datetime.utcnow()
        self.storage.write('README.rst', 'This is a readme.')
        try:
            difference = now - self.storage.modified('README.rst')
        except NotImplementedError:
            pytest.skip("not implemented in this storage")
        assert difference < datetime.timedelta(seconds=60)

    def test_list_is_a_generator(self):
        assert isinstance(self.storage.list(), types.GeneratorType)

    def test_list_should_yield_nothing_if_storage_is_empty(self):
        filenames = list(self.storage.list())
        assert filenames == []

    def test_list_should_yield_the_filenames_in_storage(self):
        self.storage.write('file1.txt', 'some content')
        self.storage.write('file2.txt', 'some content')
        self.storage.write('file3.txt', 'some content')

        filenames = list(self.storage.list())

        assert len(filenames) == 3
        assert 'file1.txt' in filenames
        assert 'file2.txt' in filenames
        assert 'file3.txt' in filenames
