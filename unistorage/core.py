# -*- coding: utf-8 -*-
"""
    unistorage.core
    ~~~~~~~~~~~~~~~

    This module contains the interfaces that storage backends should
    implement.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""


class Storage(object):
    def __init__(self, adapter):
        self.adapter = adapter

    def __contains__(self, key):
        """
        Check for the existence of a file.

        :argument key: the key of the file to check for existence
        :returns: ``True`` if `key` refers to an existing file within
          this storage, or ``False`` if the key is available for a new
          file.
        """
        return self.adapter.exists(key)

    def __getitem__(self, key):
        return File(self, key)


class File(object):
    def __init__(self, storage, key):
        self.storage = storage
        self.key = key
