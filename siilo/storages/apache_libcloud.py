# -*- coding: utf-8 -*-
"""
    siilo.storages.apache_libcloud
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""
import io
import os
import shutil
import tempfile

from siilo.exceptions import FileNotFoundError
from .base import Storage


class ApacheLibcloudStorage(Storage):
    """A storage driver for `Apache Libcloud`_

    .. _Apache Libcloud: https://libcloud.apache.org/

    Apache Libcloud is a Python library that provides a unified API for
    many popular cloud service providers. This storage driver supports
    the same storage providers as Libcloud. As of version 0.14 of
    Libcloud this includes:

    - Amazon S3
    - CloudFiles
    - Google Storage
    - KTUCloud Storage
    - Microsoft Azure
    - Nimbus.io
    - Ninefold
    - OpenStack Swift

    In order to use this storage driver you need to have Apache Libcloud
    installed. You can install it using pip::

        pip install apache-libcloud

    Internally, when you open a file, :class:`ApacheLibcloudStorage`
    will return a file-like wrapper to a temporary file. If you open the
    file for only reading or appending, :class:`ApacheLibcloudStorage`
    will also download the file from the cloud storage to the temporary
    file. Likewise, when you write to a file and close it,
    :class:`ApacheLibcloudStorage` will upload it the the cloud storage.

    Example::

        from libcloud.storage.types import Provider
        from libcloud.storage.providers import get_driver
        from siilo.storages.apache_libcloud import ApacheLibcloudStorage

        driver_cls = get_driver(Provider.S3)
        driver = driver_cls('api key', 'api secret key')

        container = driver.get_container(container_name='example-bucket')

        storage = ApacheLibcloudStorage(container)

        with storage.open('hello.txt', 'w') as f:
            f.write('Hello World!')

        with storage.open('hello.txt', 'r') as f:
            print(f.read())

    :param container:
        the :class:`~libcloud.storage.base.Container` used by this
        storage for file operations
    """
    def __init__(self, container):
        self.container = container

    def _get_object(self, name):
        from libcloud.storage.types import ObjectDoesNotExistError
        try:
            return self.container.get_object(name)
        except ObjectDoesNotExistError:
            raise FileNotFoundError(name)

    def delete(self, name):
        from libcloud.storage.types import ObjectDoesNotExistError
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

    def __repr__(self):
        return '<ApacheLibcloudStorage container={container!r}>'.format(
            container=self.container
        )


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

    def __repr__(self):
        args = [
            ('storage', self.storage),
            ('name', self.name),
            ('mode', self.mode),
        ]
        if hasattr(self, 'encoding'):
            args.append(('encoding', self.encoding))
        args = ', '.join(
            '{key}={value!r}'.format(key=key, value=value)
            for key, value in args
        )
        return '<LibcloudFile {args}>'.format(args=args)

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
