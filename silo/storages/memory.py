# -*- coding: utf-8 -*-
"""
    silo.storages.memory
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""

from silo.exceptions import FileNotFound
from . import Storage


class Memory(Storage):
    def __init__(self):
        self._files = {}

    def delete(self, name):
        try:
            del self._files[name]
        except KeyError:
            pass

    def exists(self, name):
        return name in self._files

    def list(self):
        for name in self._files:
            yield name

    def read(self, name):
        try:
            return self._files[name]
        except KeyError:
            raise FileNotFound(name)

    def size(self, name):
        try:
            return len(self._files[name])
        except KeyError:
            raise FileNotFound(name)

    def write(self, name, content):
        self._files[name] = content
