API reference
=============

.. module:: unistorage

This part of the documentation covers all the public classes and functions
in Unistorage.


Core
----

.. module:: unistorage.core
.. autoclass:: Storage
.. autoclass:: File

Adapters
--------

.. module:: unistorage.adapters.amazon
.. autoclass:: AmazonS3

.. module:: unistorage.adapters.local
.. autoclass:: Local

.. module:: unistorage.adapters.memory
.. autoclass:: Memory

Exceptions
----------

.. module:: unistorage.exceptions
.. autoclass:: UnistorageException
.. autoclass:: FileNotFound
.. autoclass:: SuspiciousFilename

Interface
---------

.. module:: unistorage.interface
.. autoclass:: Adapter
