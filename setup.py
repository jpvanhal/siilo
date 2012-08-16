from setuptools import setup, find_packages

setup(
    name='Unistorage',
    version='0.1.0',
    url='http://github.com/jpvanhal/unistorage',
    license='BSD',
    author='Janne Vanhala',
    author_email='janne.vanhala@gmail.com',
    description='File storage abstraction layer',
    long_description=open('README.rst').read() + '\n\n' +
                     open('CHANGES.rst').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
