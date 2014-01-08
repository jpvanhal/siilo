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
class FileNotFound(SiloError):
    """
    Raised when attempting to access a file that does not exist.

    :param name: name of the file
    """
    def __init__(self, name):
        self.name = force_text(name, 'utf-8')

    def __str__(self):
        return 'The file "{name}" was not found.'.format(name=self.name)


@unicode_compatible
class FileNotWithinStorage(SiloError):
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
        return 'The file "{name}" is not within the storage.'.format(
            name=self.name
        )
