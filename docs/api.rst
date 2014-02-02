API reference
=============

.. module:: silo

This part of the documentation covers all the public classes and functions
in Silo.


Storages
--------

.. module:: silo.storages.base
.. autoclass:: Storage
   :members:

.. module:: silo.storages.filesystem
.. autoclass:: FileSystemStorage

.. module:: silo.storages.apache_libcloud
.. autoclass:: ApacheLibcloudStorage

Exceptions
----------

.. module:: silo.exceptions
.. autoexception:: SiloError
.. autoexception:: FileNotFoundError
.. autoexception:: FileNotWithinStorageError
.. autoexception:: FileNotAccessibleViaURLError
