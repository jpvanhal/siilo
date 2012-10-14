# -*- coding: utf-8 -*-
"""
    unistorage.core
    ~~~~~~~~~~~~~~~

    This module contains the core API for Unistorage.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""


class Storage(object):
    def __init__(self, adapter):
        self.adapter = adapter

    def __contains__(self, name):
        """
        Check for the existence of a file.

        :argument name: the name of the file to check for existence
        :returns: ``True`` if `name` refers to an existing file within
          this storage, or ``False`` if the name is available for a new
          file.
        """
        return self.adapter.exists(name)

    def __getitem__(self, name):
        return File(self, name)


class File(object):
    def __init__(self, storage, name):
        self.storage = storage
        self.name = name

    @property
    def accessed(self):
        return self.storage.adapter.accessed(self.name)

    @property
    def content(self):
        return self.storage.adapter.read(self.name)

    @content.setter
    def content(self, value):
        self.storage.adapter.write(self.name, value)

    @property
    def created(self):
        return self.storage.adapter.created(self.name)

    def delete(self):
        self.storage.adapter.delete(self.name)

    @property
    def exists(self):
        return self.name in self.storage

    @property
    def modified(self):
        return self.storage.adapter.modified(self.name)

    @property
    def size(self):
        return self.storage.adapter.size(self.name)

    @property
    def url(self):
        return self.storage.adapter.url(self.name)
