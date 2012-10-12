from distutils.core import setup
import os
import re


HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'src', 'unistorage', '__init__.py')
    contents = open(filename).read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.match(pattern, contents, re.MULTILINE).group(1)


setup(
    name='Unistorage',
    version=get_version(),
    description='File storage abstraction layer',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()
    ),
    author='Janne Vanhala',
    author_email='janne.vanhala@gmail.com',
    url='http://github.com/jpvanhal/unistorage',
    packages=[
        'unistorage',
        'unistorage.adapters',
    ],
    package_data={
        '': ['LICENSE']
    },
    package_dir={
        '': 'src'
    },
    license=open('LICENSE').read(),
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
