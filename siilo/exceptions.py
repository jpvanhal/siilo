# -*- coding: utf-8 -*-
"""
    siilo.exceptions
    ~~~~~~~~~~~~~~~~

    This module contains Siilo-specific exceptions.

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from ._compat import force_text, unicode_compatible


class SiiloError(Exception):
    """
    Base class for all Siilo exceptions.
    """


class ArgumentError(SiiloError):
    pass


@unicode_compatible
class FileNotFoundError(SiiloError):
    """
    Raised when attempting to access a file that does not exist.

    :param name: name of the file
    :type name: str
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "{name}" was not found.'.format(name=self.name)


@unicode_compatible
class FileNotWithinStorageError(SiiloError):
    """
    Raised when a suspicious filename is supplied to a storage.

    This error occurs when using :class:`.FileSystemStorage` and trying
    to access a file not within the base directory::

        >>> from siilo.storages.filesystem import FileSystemStorage
        >>> storage = FileSystemStorage(base_directory='/path/to/storage/root')
        >>> storage.open('/etc/passwd')
        Traceback (most recent call last):
        FileNotWithinStorageError: The file "/etc/passwd" is not within
        the storage.

    :param name: name of the file
    :type name: str
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "{name}" is not within the storage.'.format(
            name=self.name
        )


class FileNotAccessibleViaURLError(SiiloError):
    """
    Raised when trying to get a URL for a file that is not accessible
    via a URL.

    This error occurs when using :class:`.FileSystemStorage`, with no
    :attr:`.FileSystemStorage.base_url` defined and trying to get a URL
    for a file::

        >>> from siilo.storages.filesystem import FileSystemStorage
        >>> storage = FileSystemStorage(base_directory='/path/to/storage/root')
        >>> storage.url('image.jpg')
        Traceback (most recent call last):
        FileNotAccessibleViaURLError: The file "image.jpg" is not accessible
        via a URL.

    :param name: name of the file
    :type name: str
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "{name}" is not accessible via a URL.'.format(
            name=self.name
        )
