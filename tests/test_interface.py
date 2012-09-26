# import time

# class StorageTestCase(object):

#     def create_storage(self):
#         """
#         Create a new storage instance.

#         This method is used in the tests to get an instance of the
#         storage class under test. The tests assume that the storage is
#         empty i.e. it does not contain any files.

#         :return: a :class:`unistorage.core.Storage` instance
#         """
#         raise NotImplementedError

#     def _get_path(self):
#         return 'unistorage-test/test-%s.txt' % time.time()

#     def setup_method(self, method):
#         self.storage = self.create_storage()

#     def test_exists_returns_false_for_nonexisting_file(self):
#         assert not self.storage.exists('test.txt')

#     def test_exists_returns_true_for_existing_file(self):
#         self.storage.save('test.txt', 'test content')
#         assert self.storage.exists('test.txt')

#     def
