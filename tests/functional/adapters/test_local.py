import shutil
import tempfile

from .lib import FunctionalTestCase


class TestLocal(FunctionalTestCase):
    def make_adapter(self):
        from silo.adapters.local import Local
        return Local(directory=tempfile.mkdtemp('silo-test'))

    def teardown_method(self, method):
        shutil.rmtree(self.adapter.directory)
