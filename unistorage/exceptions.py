# -*- coding: utf-8 -*-
"""
    unistorage.exceptions
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains Unistorage-specific exceptions.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""


class UnistorageException(Exception):
    """
    Base class for all Unistorage exceptions.
    """


class FileNotFound(UnistorageException):
    """An attempt to access a file that does not exist."""

    def __init__(self, name):
        self.name = name
        super(FileNotFound, self).__init__(
            'The file "%s" was not found.' % name
        )


class FileExistsError(UnistorageException):
    """The file already existed."""


class PermissionError(UnistorageException):
    pass


class SuspiciousFilename(UnistorageException):
    """
    Raised when a suspicious filename is supplied to an adapter.

    This error can occur in when using the
    :class:`unistorage.adapters.local.Local` adapter and the filename is
    not within the base directory.
    """

    def __init__(self, name):
        self.name = name
        super(SuspiciousFilename, self).__init__(
            'The file "%s" is not within the storage.' % name
        )
