import shutil
import tempfile

from .lib import FunctionalTestCase


class TestLocal(FunctionalTestCase):
    def make_adapter(self):
        from unistorage.adapters.local import Local
        return Local(directory=tempfile.mkdtemp('unistorage-test'))

    def teardown_method(self, method):
        shutil.rmtree(self.adapter.directory)
