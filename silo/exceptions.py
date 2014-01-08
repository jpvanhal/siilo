# -*- coding: utf-8 -*-
"""
    silo.exceptions
    ~~~~~~~~~~~~~~~

    This module contains Silo-specific exceptions.

    :copyright: (c) 2014 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import unicode_literals

from .compat import force_text, unicode_compatible


class SiloException(Exception):
    """
    Base class for all Silo exceptions.
    """


@unicode_compatible
class FileNotFound(SiloException):
    """
    Raised when attempting to access a file that does not exist.

    :param name: name of the file
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "%s" was not found.' % self.name


@unicode_compatible
class FileNotWithinStorage(SiloException):
    """
    Raised when a suspicious filename is supplied to an storage.

    This error can occur when using the
    :class:`silo.storages.filesystem.FileSystemStorage` storage and the
    filename is not within the base directory.

    :param name: name of the file
    :type name: str
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "%s" is not within the storage.' % self.name
