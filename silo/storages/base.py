# -*- coding: utf-8 -*-
"""
    silo.storages.base
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""


class Storage(object):

    def delete(self, name):
        """
        Delete the file referenced by ``name``.

        :param name: the name of the file to be deleted
        :type name: str
        :raises silo.exceptions.FileNotFoundError: if a file with the
          given `name` does not exist
        :raises NotImplementedError: if the storage system does not
          support file deletion
        """
        raise NotImplementedError

    def exists(self, name):
        """
        Check for the existence of a file.

        :param name: the name of the file to check for existence
        :type name: str
        :return: ``True`` if `name` refers to an existing file within
          this storage, or ``False`` if the name is available for a new
          file.
        :rtype: bool
        """
        raise NotImplementedError

    def open(self, name, mode='rb'):
        """
        Open a file.

        :param name: the name of the file to be opened
        :type name: str
        :param mode: a string indicating how the file should be opened
        :type mode: str
        :raises silo.exceptions.FileNotFoundError: if a file with the
          given `name` does not exist
        """
        raise NotImplementedError

    def size(self, name):
        """
        Return the size of a file in bytes.

        :param name: the name of the file
        :type name: str
        :return: the size of the file in bytes
        :rtype: int
        :raises silo.exceptions.FileNotFoundError: if a file with the
          given `name` does not exist
        :raises NotImplementedError: if the storage system is not able
          to return the file size
        """
        raise NotImplementedError

    def url(self, name):
        """
        Return the URL where the file referenced by ``name`` can be
        accessed.

        :param name: the name of the file
        :type name: str
        :return: the URL where file can be accessed
        :rtype: str
        :raises NotImplementedError: if the storage system does not
          support access by URL
        """
        raise NotImplementedError
