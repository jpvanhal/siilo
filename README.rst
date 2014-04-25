Silo
====

.. image:: http://img.shields.io/travis/jpvanhal/silo/master.svg
   :target: http://travis-ci.org/jpvanhal/silo

.. image:: http://img.shields.io/coveralls/jpvanhal/silo/master.svg
  :target: https://coveralls.io/r/jpvanhal/silo?branch=master

.. image:: http://img.shields.io/pypi/dm/silo.svg
  :target: https://pypi.python.org/pypi/silo

.. image:: http://img.shields.io/pypi/v/silo.svg
  :target: https://pypi.python.org/pypi/silo

Silo is a file abstraction layer for Python. It is inspired by `Django's File
storage API`_, but is framework agnostic.

.. _Django's File storage API:
   https://docs.djangoproject.com/en/dev/ref/files/storage/

Silo supports for the following file storages:

- Local Filesystem
- Apache Libcloud
- Amazon S3

Silo has the following goals:

- to be compatible with Python’s file API
- to support both Python 2 and 3
- to have full unit test coverage.

You can install the library with pip::

    pip install silo

Resources
---------

* `Documentation <http://silo.readthedocs.org>`_
* `Bug Tracker <http://github.com/jpvanhal/silo/issues>`_
* `Code <http://github.com/jpvanhal/silo>`_
* `Development Version <http://github.com/jpvanhal/silo/zipball/master#egg=silo-dev>`_
