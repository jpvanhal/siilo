# -*- coding: utf-8 -*-
"""
    silo.adapters.amazon
    ~~~~~~~~~~~~~~~~~~~~

    This module an adapter for Amazon Simple Storage Service (S3).

    :copyright: (c) 2014 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime, timedelta
from email.utils import parsedate_tz

from silo.exceptions import FileNotFound
from silo.interface import Adapter


class AmazonS3(Adapter):
    """
    An adapter for Amazon Simple Storage Service (S3).

    This adapter requires an boto_ library to be installed. You can
    install it by executing the following command in the terminal::

        pip install boto

    .. _boto: https://github.com/boto/boto

    Constructor arguments are as follows:

    :type access_key: str
    :param access_key: your Amazon Web Services access key id

    :type secret_key: str
    :param secret_key: your Amazon Web Services secret access key

    :type bucket_name: str
    :param bucket_name: your Amazon S3 bucket name

    :type use_query_auth: bool
    :param use_query_auth: :method:`url` should use query string
        authentication to sign the URL. This is useful for enabling
        direct access to private Amazon S3 data without proxying the
        request. Defaults to ``True``.

    :type querystring_expires: int
    :param querystring_expires: The number of seconds a URL signed with
        query string authentication is valid before expiring. Defaults
        to 3600 (one hour).
    """

    def __init__(self, access_key, secret_key, bucket_name,
                 use_query_auth=True, querystring_expires=3600):
        boto = self._import_boto()
        self.connection = boto.connect_s3(access_key, secret_key)
        self.bucket_name = bucket_name
        self.use_query_auth = use_query_auth
        self.querystring_expires = querystring_expires

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
        return key.size

    def list(self):
        for key in self.bucket.list():
            yield key.name

    def modified(self, name):
        key = self.bucket.get_key(name)
        if not key:
            raise FileNotFound(name)
        t = parsedate_tz(key.last_modified)
        return datetime(*t[:7]) - timedelta(seconds=t[-1])

    def url(self, name):
        return self.connection.generate_url(
            expires_in=self.querystring_expires,
            method='GET',
            bucket=self.bucket_name,
            key=name,
            query_auth=self.use_query_auth
        )
