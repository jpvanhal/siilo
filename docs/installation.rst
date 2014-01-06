Installation
============

This part of the documentation covers the installation of Silo.

Supported platforms
-------------------

Silo has been tested against the following Python platforms.

- cPython 2.6
- cPython 2.7
- cPython 3.1
- cPython 3.2
- PyPy_ 1.8

.. _PyPy: http://pypy.org/

Installing an official release
------------------------------

You can install the most recent official Silo version using
pip_::

    pip install silo

.. _pip: http://www.pip-installer.org/

Installing the development version
----------------------------------

To install the latest version of Silo, you need first obtain a
copy of the source. You can do that by cloning the git_ repository::

    git clone git://github.com/jpvanhal/silo.git

Then you can install the source distribution using the ``setup.py``
script::

    cd silo
    python setup.py install

.. _git: http://git-scm.org/

Checking the installation
-------------------------

To check that Silo has been properly installed, type ``python``
from your shell. Then at the Python prompt, try to import Silo,
and check the installed version:

.. parsed-literal::

    >>> import silo
    >>> silo.__version__
    |release|
