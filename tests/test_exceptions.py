# -*- coding: utf-8 -*-
import pytest

from siilo._compat import text_type, force_bytes, force_text
from siilo.exceptions import (
    FileNotAccessibleViaURLError,
    FileNotFoundError,
    FileNotWithinStorageError,
    SiiloError,
)


@pytest.mark.parametrize(
    ('cls', 'name', 'message'),
    [
        (
            FileNotAccessibleViaURLError,
            'README.rst',
            'The file "README.rst" is not accessible via a URL.'
        ),
        (
            FileNotFoundError,
            'README.rst',
            'The file "README.rst" was not found.'
        ),
        (
            FileNotFoundError,
            force_bytes('Äö'),
            'The file "Äö" was not found.'
        ),
        (
            FileNotWithinStorageError,
            '/etc/passwd',
            'The file "/etc/passwd" is not within the storage.'
        ),
        (
            FileNotWithinStorageError,
            force_bytes('../Äö'),
            'The file "../Äö" is not within the storage.'
        ),
    ]
)
class TestExceptions(object):
    @pytest.fixture
    def exception(self, cls, name, message):
        return cls(name)

    def test_constructor_sets_name(self, exception, name, message):
        assert exception.name == force_text(name)

    def test_string_representation(self, exception, name, message):
        assert text_type(exception) == force_text(message)

    def test_is_silo_exception(self, exception, name, message):
        assert isinstance(exception, SiiloError)
