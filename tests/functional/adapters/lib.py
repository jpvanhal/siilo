import datetime
import types

import pytest

from unistorage.exceptions import FileNotFound


@pytest.mark.functional
class FunctionalTestCase(object):
    def make_adapter(self):
        raise NotImplementedError

    def setup_method(self, method):
        self.adapter = self.make_adapter()

    def test_read_fails_when_reading_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            self.adapter.read('README.rst')
            assert exc.name == 'README.rst'

    def test_writing_and_reading(self):
        self.adapter.write('README.rst', 'This is a readme.')
        content = self.adapter.read('README.rst')
        assert content == 'This is a readme.'

    def test_write_updates_existing_file(self):
        self.adapter.write('README.rst', 'This is a readme.')
        self.adapter.write('README.rst', 'This is an updated readme.')
        content = self.adapter.read('README.rst')
        assert content == 'This is an updated readme.'

    def test_checking_file_existence(self):
        assert not self.adapter.exists('README.rst')
        self.adapter.write('README.rst', 'This is a readme.')
        assert self.adapter.exists('README.rst')

    def test_writing_and_deleting(self):
        self.adapter.write('README.rst', 'This is a readme.')
        assert self.adapter.exists('README.rst')
        self.adapter.delete('README.rst')
        assert not self.adapter.exists('README.rst')

    def test_delete_fails_when_deleting_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            self.adapter.delete('README.rst')
            assert exc.name == 'README.rst'

    def test_size_returns_file_size(self):
        self.adapter.write('README.rst', 'This is a readme.')
        assert self.adapter.size('README.rst') == 17

    def test_size_fails_when_accessing_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            self.adapter.size('README.rst')
            assert exc.name == 'README.rst'

    def test_modified_fails_when_accessing_non_existing_file(self):
        with pytest.raises(FileNotFound) as exc:
            try:
                self.adapter.modified('README.rst')
                assert exc.name == 'README.rst'
            except NotImplementedError:
                pytest.skip("not implemented in this adapter")

    def test_modified_returns_files_modified_time(self):
        now = datetime.datetime.utcnow()
        self.adapter.write('README.rst', 'This is a readme.')
        try:
            difference = now - self.adapter.modified('README.rst')
        except NotImplementedError:
            pytest.skip("not implemented in this adapter")
        assert difference < datetime.timedelta(seconds=1)

    def test_list_is_a_generator(self):
        assert isinstance(self.adapter.list(), types.GeneratorType)

    def test_list_should_yield_nothing_if_storage_is_empty(self):
        filenames = list(self.adapter.list())
        assert filenames == []

    def test_list_should_yield_the_filenames_in_storage(self):
        self.adapter.write('file1.txt', 'some content')
        self.adapter.write('file2.txt', 'some content')
        self.adapter.write('file3.txt', 'some content')

        filenames = list(self.adapter.list())

        assert len(filenames) == 3
        assert 'file1.txt' in filenames
        assert 'file2.txt' in filenames
        assert 'file3.txt' in filenames
