from distutils.core import setup

import unistorage

setup(
    name='Unistorage',
    version=unistorage.__version__,
    description='File storage abstraction layer',
    long_description=open('README.rst').read() + '\n' +
                     open('CHANGES.rst').read(),
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
