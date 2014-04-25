# -*- coding: utf-8 -*-
"""
    siilo.compat
    ~~~~~~~~~~~~

    :copyright: (c) 2014 by Janne Vanhala.
    :license: MIT, see LICENSE for more details.
"""

import sys
try:
    from urlparse import urljoin, urlunparse
    from urllib import quote
except ImportError:
    from urllib.parse import urljoin, urlunparse, quote  # noqa

is_py3 = sys.version_info[0] > 2

if is_py3:
    binary_type = bytes
    text_type = str
else:
    binary_type = str
    text_type = unicode


def force_text(s, encoding='utf-8'):
    if isinstance(s, text_type):
        return s
    return s.decode(encoding)


def force_bytes(s, encoding='utf-8'):
    if isinstance(s, binary_type):
        return s
    return s.encode(encoding)


def unicode_compatible(cls):
    """
    A decorator that defines ``__str__`` and ``__unicode__`` methods
    under Python 2.
    """
    if not is_py3:
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return cls
