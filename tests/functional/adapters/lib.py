from __future__ import with_statement

import datetime
import types

import pytest

from unistorage.exceptions import FileNotFound


class FunctionalTestCase(object):
    def test_read_fails_when_reading_non_existing_file(self):
        adapter = self.make_adapter()
        with pytest.raises(FileNotFound):
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
        with pytest.raises(FileNotFound):
            adapter.delete('README.rst')

    def test_size_returns_file_size(self):
        adapter = self.make_adapter()
        adapter.write('README.rst', 'This is a readme.')
        assert adapter.size('README.rst') == 17

    def test_size_fails_when_accessing_non_existing_file(self):
        adapter = self.make_adapter()
        with pytest.raises(FileNotFound):
            adapter.size('README.rst')

    def test_modified_fails_when_accessing_non_existing_file(self):
        adapter = self.make_adapter()
        with pytest.raises(FileNotFound):
            try:
                adapter.modified('README.rst')
            except NotImplementedError:
                pytest.skip("not implemented in this adapter")

    def test_modified_returns_files_modified_time(self):
        adapter = self.make_adapter()
        now = datetime.datetime.utcnow()
        adapter.write('README.rst', 'This is a readme.')
        try:
            difference = now - adapter.modified('README.rst')
        except NotImplementedError:
            pytest.skip("not implemented in this adapter")
        assert difference < datetime.timedelta(seconds=1)

    def test_list_is_a_generator(self):
        adapter = self.make_adapter()
        assert isinstance(adapter.list(), types.GeneratorType)

    def test_list_should_yield_nothing_if_storage_is_empty(self):
        adapter = self.make_adapter()
        filenames = list(adapter.list())
        assert filenames == []

    def test_list_should_yield_the_filenames_in_storage(self):
        adapter = self.make_adapter()

        adapter.write('file1.txt', 'some content')
        adapter.write('file2.txt', 'some content')
        adapter.write('file3.txt', 'some content')

        filenames = list(adapter.list())

        assert len(filenames) == 3
        assert 'file1.txt' in filenames
        assert 'file2.txt' in filenames
        assert 'file3.txt' in filenames


FunctionalTestCase = pytest.mark.functional(FunctionalTestCase)
