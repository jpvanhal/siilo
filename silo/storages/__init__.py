# -*- coding: utf-8 -*-
"""
    silo.storages
    ~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""


class Storage(object):

    def delete(self, name):
        """
        Delete the file referenced by ``name``.

        :param str name: the name of the file to be deleted
        :raises storage.exc.FileNotFoundError: if a file with the given
          `name` does not exist
        :raises NotImplementedError: if the storage system does not
          support file deletion
        """
        raise NotImplementedError

    def exists(self, name):
        """
        Check for the existence of a file.

        :param str name: the name of the file to check for existence
        :return: ``True`` if `name` refers to an existing file within
          this storage, or ``False`` if the name is available for a new
          file.
        :rtype: bool
        """
        raise NotImplementedError

    def open(self, name, mode='rb'):
        """
        Open a file.

        :param str name: the name of the file to be opened
        :param str mode: a string indicating how the file should be
          opened
        :raises storage.exc.FileNotFoundError: if a file with the given
          `name` does not exist
        """
        raise NotImplementedError

    def size(self, name):
        """
        Return the size of a file in bytes.

        :param str name: the name of the file
        :return: the size of the file in bytes
        :rtype: int
        :raises storage.exc.FileNotFoundError: if a file with the given
          `name` does not exist
        :raises NotImplementedError: if the storage system is not able
          to return the file size
        """
        raise NotImplementedError

    def url(self, name):
        """
        Return the URL where the file referenced by ``name`` can be
        accessed.

        :param str name: the name of the file
        :return: the URL where file can be accessed
        :rtype: str
        :raises storage.exc.FileNotFoundError: if a file with the given
          `name` does not exist
        :raises NotImplementedError: if the storage system does not
          support access by URL
        """
        raise NotImplementedError
