import pytest
from flexmock import flexmock


def get_adapter_class():
    from unistorage.adapters.amazon import AmazonS3
    return AmazonS3


def make_adapter(*args, **kwargs):
    AmazonS3 = get_adapter_class()
    return AmazonS3(*args, **kwargs)


@pytest.mark.unit
class TestAmazonS3(object):
    def setup_method(self, method):
        pytest.importorskip("boto")

    def test_constructor_creates_s3_connection_from_credentials(self):
        AmazonS3 = get_adapter_class()

        fake_boto = flexmock()
        (
            flexmock(AmazonS3)
            .should_receive('_import_boto')
            .and_return(fake_boto)
            .once()
        )

        fake_connection = flexmock()
        (
            fake_boto
            .should_receive('connect_s3')
            .with_args('TEST_ID', 'TEST_SECRET')
            .and_return(fake_connection)
            .once()
        )
        adapter = AmazonS3('TEST_ID', 'TEST_SECRET', 'test-bucket')
        assert adapter.connection is fake_connection

    def test_contructors_sets_bucket_name(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        assert adapter.bucket_name == 'test-bucket'

    def test_get_or_create_bucket_retrieves_the_bucket_if_it_exists(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        fake_bucket = flexmock()
        (
            flexmock(adapter.connection)
            .should_receive('get_bucket')
            .with_args('test-bucket')
            .and_return(fake_bucket)
            .once()
        )
        bucket = adapter._get_or_create_bucket()
        assert bucket is fake_bucket

    def test_get_or_create_bucket_creates_the_bucket_unless_it_exists(self):
        from boto.exception import S3ResponseError

        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        (
            flexmock(adapter.connection)
            .should_receive('get_bucket')
            .with_args('test-bucket')
            .and_raise(S3ResponseError, 404, 'Not Found', '')
            .once()
        )
        fake_bucket = flexmock()
        (
            flexmock(adapter.connection)
            .should_receive('create_bucket')
            .with_args('test-bucket')
            .and_return(fake_bucket)
            .once()
        )
        bucket = adapter._get_or_create_bucket()
        assert bucket is fake_bucket

    def test_get_or_create_bucket_fails_on_permission_error(self):
        from boto.exception import S3ResponseError

        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        (
            flexmock(adapter.connection)
            .should_receive('get_bucket')
            .with_args('test-bucket')
            .and_raise(S3ResponseError, 403, 'Forbidden', '')
            .once()
        )
        (
            flexmock(adapter.connection)
            .should_receive('create_bucket')
            .never()
        )
        with pytest.raises(S3ResponseError):
            adapter._get_or_create_bucket()

    def test_bucket_delegates_to_get_or_create_bucket(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        fake_bucket = flexmock()
        (
            flexmock(adapter)
            .should_receive('_get_or_create_bucket')
            .and_return(fake_bucket)
            .once()
        )
        assert adapter.bucket is fake_bucket
        assert adapter._bucket is fake_bucket

    def test_bucket_uses_cached_bucket_if_present(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        adapter._bucket = flexmock()
        (
            flexmock(adapter)
            .should_receive('_get_or_create_bucket')
            .never()
        )
        assert adapter.bucket is adapter._bucket

    def test_exists_returns_false_if_file_does_not_exist(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        adapter._bucket = flexmock()
        fake_key = flexmock()
        (
            flexmock(adapter.bucket)
            .should_receive('new_key')
            .with_args('README.rst')
            .and_return(fake_key)
            .once()
        )
        (
            fake_key
            .should_receive('exists')
            .and_return(False)
            .once()
        )
        assert adapter.exists('README.rst') is False

    def test_exists_returns_false_if_file_does_exists(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        adapter._bucket = flexmock()
        fake_key = flexmock()
        (
            flexmock(adapter.bucket)
            .should_receive('new_key')
            .with_args('README.rst')
            .and_return(fake_key)
            .once()
        )
        (
            fake_key
            .should_receive('exists')
            .and_return(True)
            .once()
        )
        assert adapter.exists('README.rst') is True

    def test_delete_delegates_to_buckets_delete_key(self):
        adapter = make_adapter('TEST_ID', 'TEST_SECRET', 'test-bucket')
        adapter._bucket = flexmock()
        (
            flexmock(adapter.bucket)
            .should_receive('delete_key')
            .with_args('README.rst')
            .once()
        )
        adapter.delete('README.rst')
