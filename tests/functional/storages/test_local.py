import shutil
import tempfile

from .lib import FunctionalTestCase


class TestLocal(FunctionalTestCase):
    def make_storage(self):
        from silo.storages.local import Local
        return Local(directory=tempfile.mkdtemp('silo-test'))

    def teardown_method(self, method):
        shutil.rmtree(self.storage.directory)
