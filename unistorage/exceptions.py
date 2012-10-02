# -*- coding: utf-8 -*-
"""
    unistorage.exceptions
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains Unistorage-specific exceptions.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""
from __future__ import unicode_literals

from .compat import force_text, unicode_compatible


class UnistorageException(Exception):
    """
    Base class for all Unistorage exceptions.
    """


@unicode_compatible
class FileNotFound(UnistorageException):
    """
    Raised when attempting to access a file that does not exist.

    :param name: name of the file
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "%s" was not found.' % self.name


class FileExistsError(UnistorageException):
    """The file already existed."""


class PermissionError(UnistorageException):
    pass


@unicode_compatible
class SuspiciousFilename(UnistorageException):
    """
    Raised when a suspicious filename is supplied to an adapter.

    This error can occur when using the
    :class:`unistorage.adapters.local.Local` adapter and the filename is
    not within the base directory.

    :param name: name of the file
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "%s" is not within the storage.' % self.name
