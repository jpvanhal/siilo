import os
import time
import uuid

import pytest

from .lib import FunctionalTestCase


class TestAmazonS3(FunctionalTestCase):
    def make_adapter(self):
        from silo.adapters.amazon import AmazonS3

        pytest.importorskip("boto")

        try:
            access_key = os.environ['AWS_ACCESS_KEY']
            secret_key = os.environ['AWS_SECRET_KEY']
        except KeyError:
            pytest.skip()

        adapter = AmazonS3(
            access_key=access_key,
            secret_key=secret_key,
            bucket_name='silo-test-%s' % uuid.uuid4()
        )

        self._ensure_bucket_exists(adapter)

        return adapter

    def teardown_adapter(self, adapter):
        bucket = adapter.bucket
        for key in bucket.list():
            key.delete()
        adapter.connection.delete_bucket(bucket.name)

    def _ensure_bucket_exists(self, adapter):
        """
        Create the bucket specified in the given adapter, and ensure it
        exists before returning.

        There is sometimes a short delay before the bucket is actually
        created in AmazonS3 after calling
        :method:`boto.s3.bucket.Bucket.create_bucket`. Thus the Amazon
        S3 tests could fail randomly due to the bucket being found. This
        method works around the problem by blocking until the bucket
        truly exists.

        :param adapter: a :class:`silo.adapters.amazon.AmazonS3` instance
        """
        from boto.exception import S3ResponseError

        adapter.connection.create_bucket(adapter.bucket_name)
        while True:
            try:
                adapter.connection.get_bucket(adapter.bucket_name)
            except S3ResponseError as exc:
                if exc.status != 404:
                    raise
                time.sleep(0.5)
            else:
                break
