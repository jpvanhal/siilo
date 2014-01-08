API reference
=============

.. module:: silo

This part of the documentation covers all the public classes and functions
in Silo.


Core
----

.. module:: silo.core
.. autoclass:: Storage
.. autoclass:: File

Adapters
--------

.. module:: silo.storages.amazon
.. autoclass:: AmazonS3

.. module:: silo.storages.filesystem
.. autoclass:: FileSystemStorage

.. module:: silo.storages.memory
.. autoclass:: Memory

Exceptions
----------

.. module:: silo.exceptions
.. autoclass:: SiloException
.. autoclass:: FileNotFound
.. autoclass:: FileNotWithinStorage
