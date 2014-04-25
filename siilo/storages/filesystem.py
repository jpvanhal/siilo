# -*- coding: utf-8 -*-
"""
    siilo.storages.filesystem
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""

from functools import wraps
import errno
import io
import os

from .._compat import urljoin, quote
from siilo.exceptions import (
    FileNotAccessibleViaURLError,
    FileNotFoundError,
    FileNotWithinStorageError
)
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

    Example::

        from siilo.storages.filesystem import FileSystemStorage

        storage = FileSystemStorage(
            base_directory='/path/to/uploads',
            base_url='http://media.example.com/'
        )

        with storage.open('hello.txt', 'w') as f:
            f.write('Hello World!')

        assert storage.url('hello.txt') == 'http://media.example.com/hello.txt'

    :param base_directory:
        the directory where the file storage is located in.
    :param base_url:
        URL that serves the files in this file storage.
    """
    def __init__(self, base_directory, base_url=None):
        self.base_directory = base_directory
        self.base_url = base_url

    @property
    def base_directory(self):
        return self._base_directory

    @base_directory.setter
    def base_directory(self, value):
        self._base_directory = self._normalize_path(value)

    @_ensure_file_exists
    def delete(self, name):
        os.remove(self._compute_path(name))

    def exists(self, name):
        return os.path.exists(self._compute_path(name))

    @_ensure_file_exists
    def open(self, name, mode='rb'):
        path = self._compute_path(name)
        self._ensure_path_exists_for_write_modes(path, mode)
        return io.open(path, mode)

    @_ensure_file_exists
    def size(self, name):
        return os.path.getsize(self._compute_path(name))

    def url(self, name):
        if self.base_url is None:
            raise FileNotAccessibleViaURLError(name)
        return urljoin(self.base_url, quote(name))

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
            :attr:`base_directory`.
        """
        path = self._normalize_path(os.path.join(self.base_directory, name))
        if not path.startswith(self.base_directory):
            raise FileNotWithinStorageError(name)
        return path

    def _ensure_path_exists_for_write_modes(self, path, mode):
        base_path = os.path.dirname(path)
        is_write_mode = 'a' in mode or 'w' in mode
        if is_write_mode:
            self._ensure_path_exists(base_path)

    def _ensure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    def __repr__(self):
        return '<FileSystemStorage base_directory={base_directory!r}>'.format(
            base_directory=self.base_directory
        )
