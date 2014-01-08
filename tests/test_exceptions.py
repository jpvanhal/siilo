# -*- coding: utf-8 -*-
from silo.compat import text_type, force_bytes, force_text


class TestFileNotFound(object):
    @staticmethod
    def make_exception(*args, **kwargs):
        from silo.exceptions import FileNotFound
        return FileNotFound(*args, **kwargs)

    def test_constructor_sets_name(self):
        exc = self.make_exception('README.rst')
        assert exc.name == 'README.rst'

    def test_string_representation(self):
        exc = self.make_exception('README.rst')
        assert (
            text_type(exc) ==
            force_text('The file "README.rst" was not found.')
        )

    def test_string_representation_when_name_is_bytes_and_non_ascii(self):
        exc = self.make_exception(force_bytes('Äö'))
        assert text_type(exc) == force_text('The file "Äö" was not found.')

    def test_is_silo_exception(self):
        from silo.exceptions import SiloException
        exc = self.make_exception('README.rst')
        assert isinstance(exc, SiloException)


class TestFileNotWithinStorage(object):
    @staticmethod
    def make_exception(*args, **kwargs):
        from silo.exceptions import FileNotWithinStorage
        return FileNotWithinStorage(*args, **kwargs)

    def test_constructor_sets_name(self):
        exc = self.make_exception('../etc/passwd')
        assert exc.name == '../etc/passwd'

    def test_string_representation(self):
        exc = self.make_exception('../etc/passwd')
        assert (
            text_type(exc) ==
            force_text('The file "../etc/passwd" is not within the storage.')
        )

    def test_string_representation_when_name_is_bytes_and_non_ascii(self):
        exc = self.make_exception(force_bytes('../Äö'))
        assert (
            text_type(exc) ==
            force_text('The file "../Äö" is not within the storage.')
        )

    def test_is_silo_exception(self):
        from silo.exceptions import SiloException
        exc = self.make_exception('../etc/passwd')
        assert isinstance(exc, SiloException)
