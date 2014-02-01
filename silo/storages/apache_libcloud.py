# -*- coding: utf-8 -*-
"""
    silo.storages.apache_libcloud
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""
import io
import os
import shutil
import tempfile

from libcloud.storage.types import ObjectDoesNotExistError

from silo.exceptions import FileNotFoundError
from .base import Storage


class ApacheLibcloudStorage(Storage):
    def __init__(self, container):
        self.container = container

    def _get_object(self, name):
        try:
            return self.container.get_object(name)
        except ObjectDoesNotExistError:
            raise FileNotFoundError(name)

    def delete(self, name):
        obj = self._get_object(name)
        try:
            obj.delete()
        except ObjectDoesNotExistError:
            raise FileNotFoundError(name)

    def exists(self, name):
        try:
            self._get_object(name)
        except FileNotFoundError:
            return False
        return True

    def open(self, name, mode='r', encoding=None):
        return LibcloudFile(
            storage=self,
            name=name,
            mode=mode,
            encoding=encoding
        )

    def size(self, name):
        obj = self._get_object(name)
        return obj.size

    def url(self, name):
        obj = self._get_object(name)
        return obj.get_cdn_url()


class LibcloudFile(object):
    def __init__(self, storage, name, mode='r', encoding=None):
        self.storage = storage
        self._name = name

        self._should_download = 'r' in mode or 'a' in mode
        self._has_changed = 'w' in mode

        self._open(mode, encoding)

    def _open(self, mode, encoding):
        self._make_temporary_directory()

        if self._should_download:
            self._download_or_mark_changed(mode)

        self._stream = io.open(
            self._temporary_filename,
            mode=mode,
            encoding=encoding
        )

    def close(self):
        if not self.closed:
            self._stream.close()
            if self._has_changed:
                self._upload()
            self._remove_temporary_directory()

    @property
    def name(self):
        return self._name

    def read(self):
        return self._stream.read()

    def write(self, data):
        self._has_changed = True
        self._stream.write(data)

    def writelines(self, lines):
        self._has_changed = True
        self._stream.writelines(lines)

    closed = property(lambda self: self._stream.closed)
    encoding = property(lambda self: self._stream.encoding)
    fileno = property(lambda self: self._stream.fileno)
    flush = property(lambda self: self._stream.flush)
    isatty = property(lambda self: self._stream.isatty)
    mode = property(lambda self: self._stream.mode)
    readable = property(lambda self: self._stream.readable)
    readall = property(lambda self: self._stream.readall)
    readinto = property(lambda self: self._stream.readinto)
    readline = property(lambda self: self._stream.readline)
    readlines = property(lambda self: self._stream.readlines)
    seekable = property(lambda self: self._stream.seekable)
    tell = property(lambda self: self._stream.tell)
    writable = property(lambda self: self._stream.writable)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __iter__(self):
        return iter(self._stream)

    def _make_temporary_directory(self):
        self._temporary_directory = tempfile.mkdtemp()

    def _remove_temporary_directory(self):
        shutil.rmtree(self._temporary_directory)

    @property
    def _temporary_filename(self):
        return os.path.join(
            self._temporary_directory,
            os.path.basename(self.name)
        )

    def _download_or_mark_changed(self, mode):
        try:
            self._download()
        except FileNotFoundError:
            if 'a' in mode:
                self._has_changed = True
            else:
                raise

    def _download(self):
        with io.open(self._temporary_filename, mode='wb') as f:
            obj = self.storage._get_object(self.name)
            for data in obj.as_stream():
                f.write(data)

    def _upload(self):
        with io.open(self._temporary_filename, mode='rb') as f:
            self.storage.container.upload_object_via_stream(
                iterator=f,
                object_name=self.name
            )
