from distutils.core import setup
import os
import re


HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'siilo', '__init__.py')
    contents = open(filename).read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


setup(
    name='siilo',
    version=get_version(),
    description='File storage abstraction layer',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()
    ),
    author='Janne Vanhala',
    author_email='janne.vanhala@gmail.com',
    url='http://github.com/jpvanhal/siilo',
    packages=[
        'siilo',
        'siilo.storages',
    ],
    package_data={
        '': ['LICENSE']
    },
    license=open('LICENSE').read(),
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
