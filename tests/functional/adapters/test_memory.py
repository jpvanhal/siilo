from .lib import FunctionalTestCase


class TestMemory(FunctionalTestCase):
    def make_adapter(self):
        from unistorage.adapters.memory import Memory
        return Memory()
