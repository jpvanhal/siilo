from datetime import datetime, timedelta
from pytest import mark, raises

from unistorage.exceptions import FileNotFound


@mark.functional
class FunctionalTestCase(object):
    def test_read_fails_when_reading_non_existing_file(self):
        adapter = self.make_adapter()
        with raises(FileNotFound):
            adapter.read('README.rst')

    def test_writing_and_reading(self):
        adapter = self.make_adapter()
        adapter.write('README.rst', 'This is a readme.')
        content = adapter.read('README.rst')
        assert content == 'This is a readme.'

    def test_write_updates_existing_file(self):
        adapter = self.make_adapter()
        adapter.write('README.rst', 'This is a readme.')
        adapter.write('README.rst', 'This is an updated readme.')
        content = adapter.read('README.rst')
        assert content == 'This is an updated readme.'

    def test_checking_file_existence(self):
        adapter = self.make_adapter()
        assert not adapter.exists('README.rst')
        adapter.write('README.rst', 'This is a readme.')
        assert adapter.exists('README.rst')

    def test_writing_and_deleting(self):
        adapter = self.make_adapter()
        adapter.write('README.rst', 'This is a readme.')
        assert adapter.exists('README.rst')
        adapter.delete('README.rst')
        assert not adapter.exists('README.rst')

    def test_delete_fails_when_deleting_non_existing_file(self):
        adapter = self.make_adapter()
        with raises(FileNotFound):
            adapter.delete('README.rst')

    def test_size_returns_file_size(self):
        adapter = self.make_adapter()
        adapter.write('README.rst', 'This is a readme.')
        assert adapter.size('README.rst') == 17

    def test_size_fails_when_accessing_non_existing_file(self):
        adapter = self.make_adapter()
        with raises(FileNotFound):
            adapter.size('README.rst')

    def test_modified_fails_when_accessing_non_existing_file(self):
        adapter = self.make_adapter()
        with raises(FileNotFound):
            adapter.modified('README.rst')

    def test_modified_returns_files_modified_time(self):
        adapter = self.make_adapter()
        now = datetime.utcnow()
        adapter.write('README.rst', 'This is a readme.')
        difference = now - adapter.modified('README.rst')
        assert difference < timedelta(seconds=1)
