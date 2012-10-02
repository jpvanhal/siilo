# -*- coding: utf-8 -*-
"""
    unistorage.compat
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""
from __future__ import unicode_literals

import six


def unicode_compatible(cls):
    """
    A decorator that defines ``__str__`` and ``__unicode__`` methods
    under Python 2.
    """
    if not six.PY3:
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return cls


def force_text(s, encoding='utf-8'):
    if isinstance(s, six.text_type):
        return s
    return six.text_type(s, encoding)
