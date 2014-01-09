# -*- coding: utf-8 -*-
"""
    silo.exceptions
    ~~~~~~~~~~~~~~~

    This module contains Silo-specific exceptions.

    :copyright: (c) 2014 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import unicode_literals

from ._compat import force_text, unicode_compatible


class SiloError(Exception):
    """
    Base class for all Silo exceptions.
    """


@unicode_compatible
class FileNotFoundError(SiloError):
    """
    Raised when attempting to access a file that does not exist.

    :param name: name of the file
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "{name}" was not found.'.format(name=self.name)


@unicode_compatible
class FileNotWithinStorageError(SiloError):
    """
    Raised when a suspicious filename is supplied to a storage.

    This error occurs when using :class:`.FileSystemStorage` and trying
    to access a file not within the base directory::

        >>> from silo.storages.filesystem import FileSystemStorage
        >>> storage = FileSystemStorage(directory='/path/to/storage/root')
        >>> storage.open('/etc/passwd')
        Traceback (most recent call last):
        FileNotWithinStorageError: The file "/etc/passwd" is not within the storage.

    :param name: name of the file
    :type name: str
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "{name}" is not within the storage.'.format(
            name=self.name
        )
