# -*- coding: utf-8 -*-
"""
    silo.storages.filesystem
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""

from functools import wraps
import errno
import io
import os

from silo.exceptions import FileNotFoundError, FileNotWithinStorageError
from .base import Storage


def _ensure_file_exists(method):
    @wraps(method)
    def wrapper(self, name, *args, **kwargs):
        try:
            return method(self, name, *args, **kwargs)
        except (IOError, OSError) as exc:
            if exc.errno == errno.ENOENT:
                raise FileNotFoundError(name)
            raise
    return wrapper


class FileSystemStorage(Storage):
    """
    A storage for the local filesystem.

    :param directory: the directory where the file storage is located in.
    :type directory: str
    """
    def __init__(self, directory):
        self.directory = directory

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = self._normalize_path(value)

    @_ensure_file_exists
    def delete(self, name):
        os.remove(self._compute_path(name))

    def exists(self, name):
        return os.path.exists(self._compute_path(name))

    @_ensure_file_exists
    def open(self, name, mode='rb'):
        return io.open(self._compute_path(name), mode)

    @_ensure_file_exists
    def size(self, name):
        return os.path.getsize(self._compute_path(name))

    @staticmethod
    def _normalize_path(path):
        """
        Normalize relative paths to absolute.

        :param name: the path to normalize
        :type name: str
        :return: the given path as absolute path
        """
        return os.path.abspath(path)

    def _compute_path(self, name):
        """
        Compute the file path in the filesystem from the given name.

        :param name: the filename for which the to compute the path
        :raises FileNotWithinStorage: if the computed path is not within
            :attr:`directory`.
        """
        path = self._normalize_path(os.path.join(self.directory, name))
        if not path.startswith(self.directory):
            raise FileNotWithinStorageError(name)
        return path

    def __repr__(self):
        return '<FileSystemStorage directory={directory!r}>'.format(
            directory=self.directory
        )
