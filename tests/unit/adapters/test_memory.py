import os

import pytest
from flexmock import flexmock

from unistorage.exceptions import FileNotFound


@pytest.mark.unit
class TestMemory(object):
    def get_adapter_class(self):
        from unistorage.adapters.memory import Memory
        return Memory

    def make_adapter(self, *args, **kwargs):
        Memory = self.get_adapter_class()
        return Memory(*args, **kwargs)

    def test_constructor_initializes_files_dict(self):
        adapter = self.make_adapter()
        assert adapter._files == {}

    def test_delete_does_not_fail_unless_file_exists(self):
        adapter = self.make_adapter()
        adapter.delete('README.rst')

    def test_delete_removes_file_from_files_dict(self):
        adapter = self.make_adapter()
        adapter._files['README.rst'] = 'This is a readme.'
        adapter.delete('README.rst')
        assert 'README.rst' not in adapter._files

    def test_exists_returns_false_unless_file_exists(self):
        adapter = self.make_adapter()
        assert adapter.exists('README.rst') is False

    def test_exists_returns_true_if_file_exists(self):
        adapter = self.make_adapter()
        adapter._files['README.rst'] = 'This is a readme.'
        assert adapter.exists('README.rst') is True

    def test_list_should_yield_nothing_if_storage_is_empty(self):
        adapter = self.make_adapter()
        filenames = list(adapter.list())
        assert filenames == []

    def test_list_should_yield_the_filenames_in_storage(self):
        adapter = self.make_adapter()

        adapter._files = {
            'file1.txt': 'some content',
            'file2.txt': 'some content',
            'file3.txt': 'some content'
        }

        filenames = list(adapter.list())

        assert len(filenames) == 3
        assert 'file1.txt' in filenames
        assert 'file2.txt' in filenames
        assert 'file3.txt' in filenames

    def test_read_raises_file_not_found_unless_file_exists(self):
        adapter = self.make_adapter()
        with pytest.raises(FileNotFound) as exc:
            adapter.read('README.rst')
            assert exc.name == 'README.rst'

    def test_read_returns_file_contents(self):
        adapter = self.make_adapter()
        adapter._files['README.rst'] = 'This is a readme.'
        assert adapter.read('README.rst') == 'This is a readme.'

    def test_size_raises_file_not_found_unless_file_exists(self):
        adapter = self.make_adapter()
        with pytest.raises(FileNotFound) as exc:
            adapter.size('README.rst')
            assert exc.name == 'README.rst'

    def test_size_returns_files_length_if_file_exists(self):
        adapter = self.make_adapter()
        adapter._files['README.rst'] = 'This is a readme.'
        assert adapter.size('README.rst') == 17

    def test_write_adds_file_to_the_files_dict(self):
        adapter = self.make_adapter()
        adapter.write('README.rst', 'This is a readme.')
        assert 'README.rst' in adapter._files
        assert adapter._files['README.rst'] == 'This is a readme.'
