# -*- coding: utf-8 -*-
"""
    unistorage.adapters.amazon
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module an adapter for Amazon Simple Storage Service (S3).

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.

"""
from unistorage.exceptions import FileNotFound
from unistorage.interface import Adapter


class AmazonS3(Adapter):
    """
    An adapter for Amazon Simple Storage Service (S3).

    This adapter requires an boto_ library to be installed. You can
    install it by executing the following command in the terminal::

        pip install boto

    .. _boto: https://github.com/boto/boto
    """

    def __init__(self, access_key, secret_key, bucket_name):
        """
        Construct a Amazon S3 adapter.

        :param access_key: your Amazon Web Services access key id
        :param secret_key: your Amazon Web Services secret access key
        :param bucket_name: your Amazon S3 bucket name as a string
        """
        boto = self._import_boto()
        self.connection = boto.connect_s3(access_key, secret_key)
        self.bucket_name = bucket_name

    @property
    def bucket(self):
        """
        The :class:`boto.s3.Bucket` instance with the name
        :attr:`bucket_name`.
        """
        if not hasattr(self, '_bucket'):
            self._bucket = self._get_or_create_bucket()
        return self._bucket

    def _get_or_create_bucket(self):
        """
        Retrive the bucket with the name :attr:`bucket_name`, and create
        one if necessary.

        :return: a :class:`boto.s3.Bucket` instance
        """
        from boto.exception import S3ResponseError
        try:
            bucket = self.connection.get_bucket(self.bucket_name)
        except S3ResponseError as exc:
            if exc.status != 404:
                raise
            bucket = self.connection.create_bucket(self.bucket_name)
        return bucket

    def _import_boto(self):
        """
        Import and return :module:`boto`.

        If the module cannot be imported, for example due to it not being
        installed, a :exception:`RuntimeError` is raised.
        """
        try:
            import boto
        except ImportError:
            raise RuntimeError(
                'Could not import boto. Amazon S3 adapter requires boto '
                'library to be installed. You can install it by executing '
                '``pip install boto`` in the terminal.'
            )
        return boto

    def delete(self, name):
        self.bucket.delete_key(name)

    def exists(self, name):
        key = self.bucket.new_key(name)
        return key.exists()

    def write(self, name, content):
        key = self.bucket.new_key(name)
        key.set_contents_from_string(content)

    def read(self, name):
        key = self.bucket.get_key(name)
        if not key:
            raise FileNotFound(name)
        return key.get_contents_as_string()

    def size(self, name):
        key = self.bucket.get_key(name)
        if not key:
            raise FileNotFound(name)
        metadata = key.get_metadata()
        return metadata
