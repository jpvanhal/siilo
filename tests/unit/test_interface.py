import pytest


def get_adapter_class():
    from unistorage.interface import Adapter
    return Adapter


def make_adapter(*args, **kwargs):
    Adapter = get_adapter_class()
    return Adapter(*args, **kwargs)


@pytest.mark.unit
class TestAdapter(object):
    def test_accessed_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.accessed('README.rst')

    def test_created_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.created('README.rst')

    def test_delete_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.delete('README.rst')

    def test_exists_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.exists('README.rst')

    def test_list_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.list()

    def test_modified_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.modified('README.rst')

    def test_read_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.read('README.rst')

    def test_size_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.size('README.rst')

    def test_write_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.write('README.rst', 'This is a readme.')

    def test_url_raises_not_implemented_error(self):
        adapter = make_adapter()
        with pytest.raises(NotImplementedError):
            adapter.url('README.rst')
