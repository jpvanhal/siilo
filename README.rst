Silo
==========

.. image:: https://secure.travis-ci.org/jpvanhal/silo.png?branch=master
   :target: http://travis-ci.org/jpvanhal/silo

Silo is a file storage abstraction layer for Python.

File storages supported:

- Amazon S3
- Local file system
- Memory

Usage
-----

Initialize a file storage using the Amazon S3 adapter:

.. code-block:: python

    >>> from silo import Storage
    >>> from silo.storages.amazon import AmazonS3
    >>> storage = AmazonS3(
    ...     access_key='YOUR_AWS_ACCESS_KEY_ID',
    ...     secret_key='YOUR_AWS_SECRET_ACCESS_KEY',
    ...     bucket_name='silo-test'
    ... )

Create a file:

.. code-block:: python

    >>> hello = storage['hello.txt']
    >>> hello.content = 'Hello world!'

Get a public URL to the file:

.. code-block:: python

    >>> hello.url
    'https://silo-test.s3.amazonaws.com/hello.txt?Signature=...'

Delete the file:

.. code-block:: python

    >>> hello.delete()

Installation
------------

You can install Silo with pip::

    $ pip install silo

Resources
---------

* `Documentation <http://silo.readthedocs.org>`_
* `Bug Tracker <http://github.com/jpvanhal/silo/issues>`_
* `Code <http://github.com/jpvanhal/silo>`_
* `Development Version <http://github.com/jpvanhal/silo/zipball/master#egg=silo-dev>`_
