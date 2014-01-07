import os

import pytest
from flexmock import flexmock

from silo.exceptions import FileNotFound


@pytest.mark.unit
class TestMemory(object):
    def get_storage_class(self):
        from silo.storages.memory import Memory
        return Memory

    def make_storage(self, *args, **kwargs):
        Memory = self.get_storage_class()
        return Memory(*args, **kwargs)

    def test_constructor_initializes_files_dict(self):
        storage = self.make_storage()
        assert storage._files == {}

    def test_delete_does_not_fail_unless_file_exists(self):
        storage = self.make_storage()
        storage.delete('README.rst')

    def test_delete_removes_file_from_files_dict(self):
        storage = self.make_storage()
        storage._files['README.rst'] = 'This is a readme.'
        storage.delete('README.rst')
        assert 'README.rst' not in storage._files

    def test_exists_returns_false_unless_file_exists(self):
        storage = self.make_storage()
        assert storage.exists('README.rst') is False

    def test_exists_returns_true_if_file_exists(self):
        storage = self.make_storage()
        storage._files['README.rst'] = 'This is a readme.'
        assert storage.exists('README.rst') is True

    def test_list_should_yield_nothing_if_storage_is_empty(self):
        storage = self.make_storage()
        filenames = list(storage.list())
        assert filenames == []

    def test_list_should_yield_the_filenames_in_storage(self):
        storage = self.make_storage()

        storage._files = {
            'file1.txt': 'some content',
            'file2.txt': 'some content',
            'file3.txt': 'some content'
        }

        filenames = list(storage.list())

        assert len(filenames) == 3
        assert 'file1.txt' in filenames
        assert 'file2.txt' in filenames
        assert 'file3.txt' in filenames

    def test_read_raises_file_not_found_unless_file_exists(self):
        storage = self.make_storage()
        with pytest.raises(FileNotFound) as exc:
            storage.read('README.rst')
            assert exc.name == 'README.rst'

    def test_read_returns_file_contents(self):
        storage = self.make_storage()
        storage._files['README.rst'] = 'This is a readme.'
        assert storage.read('README.rst') == 'This is a readme.'

    def test_size_raises_file_not_found_unless_file_exists(self):
        storage = self.make_storage()
        with pytest.raises(FileNotFound) as exc:
            storage.size('README.rst')
            assert exc.name == 'README.rst'

    def test_size_returns_files_length_if_file_exists(self):
        storage = self.make_storage()
        storage._files['README.rst'] = 'This is a readme.'
        assert storage.size('README.rst') == 17

    def test_write_adds_file_to_the_files_dict(self):
        storage = self.make_storage()
        storage.write('README.rst', 'This is a readme.')
        assert 'README.rst' in storage._files
        assert storage._files['README.rst'] == 'This is a readme.'
