import os

import pytest
from flexmock import flexmock

from silo.exceptions import SuspiciousFilename


@pytest.mark.unit
class TestLocal(object):
    def get_storage_class(self):
        from silo.storages.local import Local
        return Local

    def make_storage(self, *args, **kwargs):
        Local = self.get_storage_class()
        return Local(*args, **kwargs)

    def test_constructor_normalizes_and_sets_directory(self):
        Local = self.get_storage_class()
        (
            flexmock(Local)
            .should_receive('normalize_path')
            .with_args('/some/path')
            .and_return('/some/path')
            .once()
        )
        storage = Local('/some/path')
        assert storage.directory == '/some/path'

    def test_normalize_path_delegates_to_abspath(self):
        Local = self.get_storage_class()
        (
            flexmock(os.path)
            .should_receive('abspath')
            .with_args('/foo/../bar')
            .and_return('/foo/bar')
            .once()
        )
        assert Local.normalize_path('/foo/../bar') == '/foo/bar'

    def test_compute_path_joins_given_name_with_base_directory(self):
        storage = self.make_storage('/some/path')
        assert storage.compute_path('foo') == '/some/path/foo'

    def test_compute_path_fails_if_resulting_path_is_outside_base_dir(self):
        storage = self.make_storage('/some/path')
        with pytest.raises(SuspiciousFilename) as exc:
            storage.compute_path('../foo')
            assert exc.name == '../foo'
