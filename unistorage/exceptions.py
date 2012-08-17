# -*- coding: utf-8 -*-
"""
    unistorage.exceptions
    ~~~~~~~~~~~~~~~~~

    This module contains Unistorage-specific exceptions.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""


class StorageError(Exception):
    """
    Base class for Storage errors.
    """


class FileNotFoundError(StorageError):
    """The file was not found."""


class FileExistsError(StorageError):
    """The file already existed."""


class PermissionError(StorageError):
    pass
