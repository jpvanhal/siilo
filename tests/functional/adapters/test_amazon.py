import os
import uuid

import pytest

from .lib import FunctionalTestCase


class TestAmazonS3(FunctionalTestCase):
    def make_adapter(self):
        from unistorage.adapters.amazon import AmazonS3

        pytest.importorskip("boto")

        try:
            access_key = os.environ['AWS_ACCESS_KEY']
            secret_key = os.environ['AWS_SECRET_KEY']
        except KeyError:
            pytest.skip()

        return AmazonS3(
            access_key=access_key,
            secret_key=secret_key,
            bucket_name='unistorage-test-%s' % uuid.uuid4()
        )

    def teardown_adapter(self, adapter):
        bucket = adapter.bucket
        for key in bucket.list():
            key.delete()
        adapter.connection.delete_bucket(bucket.name)
