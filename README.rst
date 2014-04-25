Siilo
=====

.. image:: http://img.shields.io/travis/jpvanhal/siilo/master.svg
   :target: http://travis-ci.org/jpvanhal/siilo

.. image:: http://img.shields.io/coveralls/jpvanhal/siilo/master.svg
  :target: https://coveralls.io/r/jpvanhal/siilo?branch=master

.. image:: http://img.shields.io/pypi/dm/siilo.svg
  :target: https://pypi.python.org/pypi/siilo

.. image:: http://img.shields.io/pypi/v/siilo.svg
  :target: https://pypi.python.org/pypi/siilo

Siilo is a file storage abstraction layer for Python. It is inspired by
`Django's File storage API`_, but is framework agnostic.

.. _Django's File storage API:
   https://docs.djangoproject.com/en/dev/ref/files/storage/

Siilo supports for the following file storages:

- Local Filesystem
- Apache Libcloud
- Amazon S3

Siilo has the following goals:

- to be compatible with Python’s file API
- to support both Python 2 and 3
- to have full unit test coverage.

You can install the library with pip::

    pip install siilo

Resources
---------

* `Documentation <http://siilo.readthedocs.org>`_
* `Bug Tracker <http://github.com/jpvanhal/siilo/issues>`_
* `Code <http://github.com/jpvanhal/siilo>`_
* `Development Version <http://github.com/jpvanhal/siilo/zipball/master#egg=siilo-dev>`_
