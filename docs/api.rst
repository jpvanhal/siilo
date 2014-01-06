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

.. module:: silo.adapters.amazon
.. autoclass:: AmazonS3

.. module:: silo.adapters.local
.. autoclass:: Local

.. module:: silo.adapters.memory
.. autoclass:: Memory

Exceptions
----------

.. module:: silo.exceptions
.. autoclass:: SiloException
.. autoclass:: FileNotFound
.. autoclass:: SuspiciousFilename

Interface
---------

.. module:: silo.interface
.. autoclass:: Adapter
