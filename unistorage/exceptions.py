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
    """The file was not found."""


class FileExistsError(UnistorageException):
    """The file already existed."""


class PermissionError(UnistorageException):
    pass
