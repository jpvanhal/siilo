# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six


class TestFileNotFound(object):
    @staticmethod
    def make_exception(*args, **kwargs):
        from unistorage.exceptions import FileNotFound
        return FileNotFound(*args, **kwargs)

    def test_constructor_sets_name(self):
        exc = self.make_exception('README.rst')
        assert exc.name == 'README.rst'

    def test_string_representation(self):
        exc = self.make_exception('README.rst')
        assert six.text_type(exc) == 'The file "README.rst" was not found.'

    def test_string_representation_when_name_is_bytes_and_non_ascii(self):
        exc = self.make_exception('Äö'.encode('utf8'))
        assert six.text_type(exc) == 'The file "Äö" was not found.'

    def test_is_unistorage_exception(self):
        from unistorage.exceptions import UnistorageException
        exc = self.make_exception('README.rst')
        assert isinstance(exc, UnistorageException)


class TestSuspiciousFilename(object):
    @staticmethod
    def make_exception(*args, **kwargs):
        from unistorage.exceptions import SuspiciousFilename
        return SuspiciousFilename(*args, **kwargs)

    def test_constructor_sets_name(self):
        exc = self.make_exception('../etc/passwd')
        assert exc.name == '../etc/passwd'

    def test_string_representation(self):
        exc = self.make_exception('../etc/passwd')
        assert (
            six.text_type(exc) ==
            'The file "../etc/passwd" is not within the storage.'
        )

    def test_string_representation_when_name_is_bytes_and_non_ascii(self):
        exc = self.make_exception('../Äö'.encode('utf8'))
        assert (
            six.text_type(exc) ==
            'The file "../Äö" is not within the storage.'
        )

    def test_is_unistorage_exception(self):
        from unistorage.exceptions import UnistorageException
        exc = self.make_exception('../etc/passwd')
        assert isinstance(exc, UnistorageException)
