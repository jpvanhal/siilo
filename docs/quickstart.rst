Quickstart
==========

This page gives you an introduction to Siilo. It shows you an example of using
Siilo in the local filesystem. You can read how you can use Siilo for the
:ref:`local-filesystem`, :ref:`amazon-s3` and :ref:`apache-libcloud` in their
respective chapters.

If you do not already have Siilo installed, run this in your terminal::

    pip install siilo


To get started let's open a file in the local file system::

    >>> from siilo.storages.filesystem import FileSystemStorage
    >>> storage = FileSystemStorage('my_directory')

Now you will be able to access and modify any file within this directory using
the Siilo API. For example, to write to a file::

    >>> with storage.open('foo.txt', 'w') as f:
    ...     f.write(u'Hello World!')
    ...
    12L

Note that if ``foo.txt`` does not exist in the directory, opening the file in
the write mode ``'w'`` will create the file. If the open mode is not specified
the default mode is ``'rb'``.

To read the file we just wrote to now::

    >>> with storage.open('foo.txt') as f:
    ...     f.read()
    ...
    'Hello World!'

You can also get the size of the file::

    >>> storage.size('foo.txt')
    12

And also check if a file exists with a certain name in the base directory::

    >>> storage.exists('bar.txt')
    False
    >>> storage.exists('foo.txt')
    True

You can also delete the file using the delete method::

    >>> storage.delete('foo.txt')
    >>> storage.exists('foo.txt')
    False
