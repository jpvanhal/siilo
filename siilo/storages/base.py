# -*- coding: utf-8 -*-
"""
    siilo.storages.base
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""


class Storage(object):
    """An abstract interface for concrete storage drivers."""

    def delete(self, name):
        """Delete the file referenced by ``name``.

        If the file does not exist, raises :exc:`.FileNotFoundError`.

        If the storage system does not support file deletion, raises
        :exc:`~exceptions.NotImplementedError`.

        """
        raise NotImplementedError

    def exists(self, name):
        """Return ``True`` if the file referenced by ``name`` exists in
        the storage system, or ``False`` if the name is available for a
        new file.

        """
        raise NotImplementedError

    def open(self, name, mode='r', encoding=None):
        """Open the file referenced by ``name`` and return a
        corresponding stream.

        The optional parameters ``mode`` and ``encoding`` are the same
        as in :func:`io.open`.

        If :meth:`open` is used to open a file for reading and the file
        with the given ``name`` does not exist, :meth:`open` will raise
        :exc:`.FileNotFoundError`.

        See also: :func:`io.open`.

        """
        raise NotImplementedError

    def size(self, name):
        """Return the size of the file referenced by ``name`` in bytes.

        If the file does not exist, raises :exc:`.FileNotFoundError`.

        If the storage system is not able to return the file size,
        raises :exc:`~exceptions.NotImplementedError`.

        """
        raise NotImplementedError

    def url(self, name):
        """Return a public URL for the file referenced by ``name``.

        If the file does not exist, this function *may* raise
        :exc:`.FileNotFoundError`. However, storage system
        implementations can choose to return the URL for the file, even
        if the file does not exist, e.g. for performance reasons.

        If the storage system does not support access by URL, raises
        :exc:`~exceptions.NotImplementedError`.

        """
        raise NotImplementedError
