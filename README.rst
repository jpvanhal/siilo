Unistorage
==========

.. image:: https://secure.travis-ci.org/jpvanhal/unistorage.png?branch=master
   :target: http://travis-ci.org/jpvanhal/unistorage

Unistorage is a file storage abstraction layer for Python.

File storages supported:

- Amazon S3
- Local file system
- Memory

Usage
-----

Initialize a file storage using the Amazon S3 adapter:

.. code-block:: python

    >>> from unistorage import Storage
    >>> from unistorage.adapters import AmazonS3
    >>> adapter = AmazonS3(
    ...     access_key='YOUR_AWS_ACCESS_KEY_ID',
    ...     secret_key='YOUR_AWS_SECRET_ACCESS_KEY',
    ...     bucket_name='unistorage-test'
    ... )
    >>> storage = Storage(adapter)

Create a file:

.. code-block:: python

    >>> file = storage['hello.txt']
    >>> file.content = 'Hello world!'

Get a public URL to the file:

.. code-block:: python

    >>> print file.url
    https://unistorage-test.s3.amazonaws.com/hello.txt?Signature=...

Delete the file:

.. code-block:: python

    >>> file.delete()

Installation
------------

You can install Unistorage with pip::

    $ pip install unistorage

Resources
---------

* `Documentation <http://unistorage.readthedocs.org>`_
* `Bug Tracker <http://github.com/jpvanhal/unistorage/issues>`_
* `Code <http://github.com/jpvanhal/unistorage>`_
* `Development Version <http://github.com/jpvanhal/unistorage/zipball/master#egg=unistorage-dev>`_
