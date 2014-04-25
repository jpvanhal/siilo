=====
Siilo
=====

Siilo is a file abstraction layer for Python. It is inspired by `Django's File
storage API`_, but is framework agnostic.

.. _Django's File storage API:
   https://docs.djangoproject.com/en/dev/ref/files/storage/

Siilo supports for the following file storages:

    - :ref:`local-filesystem`
    - :ref:`apache-libcloud`
    - :ref:`amazon-s3`

Siilo has the following goals:

- to be compatible with Python's file API
- to support both Python 2 and 3
- to have full unit test coverage.

You can install the library with pip::

    pip install siilo

Contents
========

.. toctree::
   :maxdepth: 2

   quickstart
   storages/amazon_s3
   storages/apache_libcloud
   storages/filesystem
   api
   changelog
   license
