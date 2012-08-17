# -*- coding: utf-8 -*-
"""
    unistorage.core
    ~~~~~~~~~~~~~~~

    This module contains the interfaces that storage backends should
    implement.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""


class Storage(object):

    def __len__(self):
        """
        Return the number of files in this storage.
        """
        raise NotImplementedError

    def __iter__(self):
        """
        Iterate over the storage yielding each file contained in it.
        """
        raise NotImplementedError

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

    def modified(self, name):
        """
        Return the last modified time of a file.

        For storage systems that are not able to return the last
        modified time this will raise :exc:`NotImplementedError`
        instead.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        :argument name: the name of the file whose last modified time
          you want to check.
        :returns: a :class:`datetime.datetime` object
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

    def open(self, name, mode='rb'):
        """
        Return an :class:`File` instance for an existing file.

        If a file with the given `name` does not exist then a
        :exc:`storage.exc.FileNotFoundError` exception is raised.

        :argument name: the name of the file to retrieve
        :returns: a :class:`File` representing the file requested
        """
        raise NotImplementedError

    def __str__(self):
        return self.name


class File(object):

    def __init__(self, storage, name):
        self.storage = storage
        self.name = name
        self._mode = mode

    def closed(self):
        """
        A boolean indicating whether the file is closed.
        """
        raise NotImplementedError

    @property
    def mode(self):
        """
        The read/write mode for the file.
        """
        return self._mode

    @property
    def size(self):
        """
        The size of this file in bytes.
        """
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    def read(self, num_bytes=None):
        """
        Read content from the file.

        :param num_bytes: the number of bytes to read; if not specified
            the file will be read to the end.
        """
        raise NotImplementedError

    def write(self, content):
        """
        Write content to the file.

        Depending on the storage system behind the scenes, this content
        might not be fully committed until :method:`close` is called on
        the file.

        :param content: a string or `file`-like object to write to the
            file.
        """
        raise NotImplementedError

    def close(self):
        """
        Close the file.
        """
        raise NotImplementedError

    def __iter__(self):
        """
        Iterate over the file yielding one line at a time.
        """
        raise NotImplementedError

    def __len__(self):
        return self.size

    def __str__(self):
        return self.name
