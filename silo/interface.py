# -*- coding: utf-8 -*-
"""
    silo.interface
    ~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""


class Adapter(object):

    def accessed(self, name):
        """
        Return the last accessed time of a file.

        For storage systems that are not able to return the last
        accessed time this will raise :exc:`NotImplementedError`
        instead.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        :argument name: the name of the file whose last accessed time
          you want to check.
        :returns: a :class:`datetime.datetime` object
        """
        raise NotImplementedError

    def created(self, name):
        """
        Return the creation time of a file.

        For storage systems that are not able to return the creation
        time this will raise :exc:`NotImplementedError` instead.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        :argument name: the name of the file whose creation time you
          want to check.
        :returns: a :class:`datetime.datetime` object
        """
        raise NotImplementedError

    def delete(self, name):
        """
        Delete the file referenced by ``name``.

        :argument name: the name of the file to be deleted
        """
        raise NotImplementedError

    def exists(self, name):
        """
        Check for the existence of a file.

        :argument name: the name of the file to check for existence
        :returns: ``True`` if `name` refers to an existing file within
          this storage, or ``False`` if the name is available for a new
          file.
        """
        raise NotImplementedError

    def list(self):
        """
        Yield the name of each file the storage contains.
        """
        raise NotImplementedError

    def modified(self, name):
        """
        Return the last modified time of a file.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        For storage systems that are not able to return the last
        modified time this will raise :exc:`NotImplementedError`
        instead.

        :argument name: the name of the file whose last modified time
          you want to check.
        :returns: a :class:`datetime.datetime` object
        """
        raise NotImplementedError

    def read(self, name):
        """
        Read the contents of a file.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        :argument name: the name of the file to retrieve
        :returns: a string representing the file contents
        """
        raise NotImplementedError

    def size(self, name):
        """
        Return the size of a file in bytes.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        For storage systems that are not able to return the file size
        this will raise :exc:`NotImplementedError` instead.

        :argument name: the name of the file
        :returns: an integer representing the size of the file in bytes
        """
        raise NotImplementedError

    def write(self, name, content):
        """
        Write the given ``content`` to a file.

        If there already exists a file with the name ``name``, this
        method will overwrite the file.

        :argument name: the name of the file
        :argument content: a string to be written to the file
        """
        raise NotImplementedError

    def url(self, name):
        """
        Return the URL where the file referenced by ``name`` can be
        accessed.

        For storage systems that do not support access by URL this will
        raise :exc:`NotImplementedError` instead.

        :argument name: the name of the file
        :returns: a string representing the URL of the file
        """
        raise NotImplementedError
