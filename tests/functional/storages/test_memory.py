from .lib import FunctionalTestCase


class TestMemory(FunctionalTestCase):
    def make_storage(self):
        from silo.storages.memory import Memory
        return Memory()
