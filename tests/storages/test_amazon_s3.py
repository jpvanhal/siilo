# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import textwrap

try:
    from unittest import mock
except ImportError:
    import mock

import freezegun
from libcloud.storage.base import Container
from libcloud.storage.drivers.s3 import BaseS3StorageDriver
import pytest

from siilo.exceptions import ArgumentError


class TestAmazonS3Storage(object):

    @staticmethod
    def make_storage(**kwargs):
        from siilo.storages.amazon_s3 import AmazonS3Storage

        with mock.patch.object(
            BaseS3StorageDriver,
            'get_container',
            side_effect=lambda self, name: Container(name, {}, self),
            autospec=True
        ):
            return AmazonS3Storage(
                access_key_id='AKIAIOSFODNN7EXAMPLE',
                secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                bucket='examplebucket',
                **kwargs
            )

    @pytest.fixture
    def storage(self):
        return self.make_storage()

    def test_inherits_from_apache_libcloud_storage(self, storage):
        from siilo.storages.apache_libcloud import ApacheLibcloudStorage
        assert isinstance(storage, ApacheLibcloudStorage)

    def test_constructor_creates_container(self, storage):
        assert storage.container.name == 'examplebucket'

    def test_driver_is_amazon_s3_driver(self, storage):
        from libcloud.storage.drivers.s3 import S3StorageDriver
        assert isinstance(storage.container.driver, S3StorageDriver)

    def test_driver_use_correct_credentials(self, storage):
        assert storage.container.driver.key == 'AKIAIOSFODNN7EXAMPLE'
        assert (
            storage.container.driver.secret ==
            'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        )

    @pytest.mark.parametrize(
        ('region', 'host'),
        [
            ('us-east-1', 's3.amazonaws.com'),
            ('us-west-2', 's3-us-west-2.amazonaws.com'),
            ('us-west-1', 's3-us-west-1.amazonaws.com'),
            ('eu-west-1', 's3-eu-west-1.amazonaws.com'),
            ('ap-southeast-1', 's3-ap-southeast-1.amazonaws.com'),
            ('ap-northeast-1', 's3-ap-northeast-1.amazonaws.com'),
        ]
    )
    def test_driver_uses_correct_host(self, region, host):
        storage = self.make_storage(region=region)
        assert storage.container.driver.connection.host == host

    def test_raises_exception_on_unknown_region(self):
        with pytest.raises(ArgumentError) as excinfo:
            self.make_storage(region='unknown')
        assert str(excinfo.value) == (
            "Invalid value 'unknown' for region. Valid Amazon S3 regions are "
            "ap-northeast-1, ap-southeast-1, eu-west-1, us-east-1, us-west-1, "
            "us-west-2"
        )

    @pytest.mark.parametrize(
        ('attr', 'default_value'),
        [
            ('use_path_style', False),
            ('use_https', True),
            ('use_query_string_auth', False),
            ('url_expires', timedelta(hours=1)),
        ]
    )
    def test_constructor_default_arguments(self, storage, attr, default_value):
        assert getattr(storage, attr) == default_value

    @pytest.mark.parametrize(
        (
            'region',
            'use_path_style',
            'use_https',
            'use_query_string_auth',
            'url_expires',
            'key',
            'url',
        ),
        [
            (
                'eu-west-1',
                False,
                True,
                False,
                None,
                'test.txt',
                'https://examplebucket.s3-eu-west-1.amazonaws.com/test.txt',
            ),
            (
                'eu-west-1',
                True,
                False,
                False,
                None,
                'test.txt',
                'http://s3-eu-west-1.amazonaws.com/examplebucket/test.txt',
            ),
            (
                'us-east-1',
                False,
                False,
                False,
                None,
                'test.txt',
                'http://examplebucket.s3.amazonaws.com/test.txt',
            ),
            (
                'us-east-1',
                True,
                True,
                False,
                None,
                'test.txt',
                'https://s3.amazonaws.com/examplebucket/test.txt',
            ),
            (
                'us-east-1',
                False,
                True,
                True,
                timedelta(hours=24),
                'test.txt',
                (
                    'https://examplebucket.s3.amazonaws.com/test.txt?'
                    'X-Amz-Algorithm=AWS4-HMAC-SHA256&'
                    'X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20130524%2F'
                    'us-east-1%2Fs3%2Faws4_request&'
                    'X-Amz-Date=20130524T000000Z&'
                    'X-Amz-Expires=86400&'
                    'X-Amz-Signature=aeeed9bbccd4d02ee5c0109b86d86835f995330da'
                    '4c265957d157751f604d404&'
                    'X-Amz-SignedHeaders=host'
                )
            ),
            (
                'us-east-1',
                False,
                False,
                False,
                None,
                u'åöä',
                'http://examplebucket.s3.amazonaws.com/%C3%A5%C3%B6%C3%A4',
            ),
            (
                'us-east-1',
                False,
                False,
                True,
                timedelta(hours=1),
                u'åöä',
                (
                    'http://examplebucket.s3.amazonaws.com/%C3%A5%C3%B6%C3%A4?'
                    'X-Amz-Algorithm=AWS4-HMAC-SHA256&'
                    'X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20130524%2F'
                    'us-east-1%2Fs3%2Faws4_request&'
                    'X-Amz-Date=20130524T000000Z&'
                    'X-Amz-Expires=3600&'
                    'X-Amz-Signature=0921cdcbd2d64caa66dce47683e9807fef8f71ea2'
                    '404c4ae50dd02b88e69a438&'
                    'X-Amz-SignedHeaders=host'
                )
            ),
        ]
    )
    def test_url(self, region, use_path_style, use_https,
                 use_query_string_auth, url_expires, key, url):
        with freezegun.freeze_time('2013-05-24'):
            storage = self.make_storage(
                region=region,
                use_path_style=use_path_style,
                use_https=use_https,
                use_query_string_auth=use_query_string_auth,
                url_expires=url_expires
            )
            assert storage.url(key) == url

    def test_repr(self, storage):
        assert repr(storage) == "<AmazonS3Storage bucket='examplebucket'>"


@pytest.fixture(scope='session')
def signer():
    from siilo.storages.amazon_s3 import _SignerV4
    return _SignerV4(
        access_key_id='AKIAIOSFODNN7EXAMPLE',
        secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        region='us-east-1',
        service_name='s3'
    )


class TestSignerV4(object):
    @pytest.fixture
    def headers(self):
        return {
            'X-Amz-Signature': '<signature-value>',
            'X-Amz-Expires': '86400',
            'X-Amz-Date': ' 20130721T201207Z',
            'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
            'X-Amz-SignedHeaders': 'host ',
            'X-Amz-Credential': '<key>/20130721/us-east-1/s3/aws4_request',
        }

    @pytest.fixture
    def params(self):
        return {
            'prefix': 'some prefix',
            'marker': 'some marker',
            'max-keys': '20',
            'array[]': '1,2,3',
        }

    @pytest.fixture
    def s3_request(self, headers, params):
        from siilo.storages.amazon_s3 import _S3Request
        return _S3Request(
            method='GET',
            endpoint='s3.amazonaws.com',
            bucket='examplebucket',
            key='myphoto.jpg',
            headers=headers,
            params=params,
            use_https=False,
        )

    def test_canonical_query_string(self, s3_request):
        assert s3_request.canonical_query_string == (
            'array%5B%5D=1%2C2%2C3&'
            'marker=some%20marker&'
            'max-keys=20&'
            'prefix=some%20prefix'
        )

    def test_canonical_headers(self, s3_request):
        assert s3_request.canonical_headers == (
            'x-amz-algorithm:AWS4-HMAC-SHA256\n'
            'x-amz-credential:<key>/20130721/us-east-1/s3/aws4_request\n'
            'x-amz-date:20130721T201207Z\n'
            'x-amz-expires:86400\n'
            'x-amz-signature:<signature-value>\n'
            'x-amz-signedheaders:host\n'
        )

    def test_signed_headers(self, s3_request):
        assert s3_request.signed_headers == (
            'x-amz-algorithm;'
            'x-amz-credential;'
            'x-amz-date;'
            'x-amz-expires;'
            'x-amz-signature;'
            'x-amz-signedheaders'
        )

    def test_get_scope(self, signer):
        scope = '20130524/us-east-1/s3/aws4_request'
        assert signer._get_scope('20130524T000000Z') == scope


class _TestSignerV4Example(object):
    payload_sha256 = (
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    )
    timestamp = '20130524T000000Z'

    def test_canonical_request(self, signer, s3_request):
        expected = textwrap.dedent(self.canonical_request)
        actual = signer._get_canonical_request(s3_request, self.payload_sha256)
        assert actual == expected

    def test_string_to_sign(self, signer, s3_request):
        expected = textwrap.dedent(self.string_to_sign)
        actual = signer._get_string_to_sign(
            s3_request,
            self.timestamp,
            self.payload_sha256
        )
        assert actual == expected

    def test_signature(self, signer, s3_request):
        actual = signer.get_signature(
            s3_request,
            self.timestamp,
            self.payload_sha256
        )
        assert actual == self.signature


class TestSignerV4GETObjectExample(_TestSignerV4Example):
    canonical_request = '''\
        GET
        /test.txt

        host:examplebucket.s3.amazonaws.com
        range:bytes=0-9
        x-amz-content-sha256:\
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        x-amz-date:20130524T000000Z

        host;range;x-amz-content-sha256;x-amz-date
        e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

    string_to_sign = '''\
        AWS4-HMAC-SHA256
        20130524T000000Z
        20130524/us-east-1/s3/aws4_request
        7344ae5b7ee6c3e7e6b0fe0640412a37625d1fbfff95c48bbb2dc43964946972'''

    signature = (
        'f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41'
    )

    @pytest.fixture
    def s3_request(self):
        from siilo.storages.amazon_s3 import _S3Request
        return _S3Request(
            method='GET',
            endpoint='s3.amazonaws.com',
            bucket='examplebucket',
            key='test.txt',
            headers={
                'Host': 'examplebucket.s3.amazonaws.com',
                'Range': 'bytes=0-9',
                'X-Amz-Content-SHA256': (
                    'e3b0c44298fc1c149afbf4c8996fb924'
                    '27ae41e4649b934ca495991b7852b855'
                ),
                'X-Amz-Date': '20130524T000000Z',
            },
            use_https=False,
        )


class TestSignerV4PUTObjectExample(_TestSignerV4Example):
    canonical_request = '''\
        PUT
        /test%24file.text

        date:Fri, 24 May 2013 00:00:00 GMT
        host:examplebucket.s3.amazonaws.com
        x-amz-content-sha256:\
44ce7dd67c959e0d3524ffac1771dfbba87d2b6b4b4e99e42034a8b803f8b072
        x-amz-date:20130524T000000Z
        x-amz-storage-class:REDUCED_REDUNDANCY

        date;host;x-amz-content-sha256;x-amz-date;x-amz-storage-class
        44ce7dd67c959e0d3524ffac1771dfbba87d2b6b4b4e99e42034a8b803f8b072'''

    string_to_sign = '''\
        AWS4-HMAC-SHA256
        20130524T000000Z
        20130524/us-east-1/s3/aws4_request
        9e0e90d9c76de8fa5b200d8c849cd5b8dc7a3be3951ddb7f6a76b4158342019d'''

    signature = (
        '98ad721746da40c64f1a55b78f14c238d841ea1380cd77a1b5971af0ece108bd'
    )

    payload_sha256 = (
        '44ce7dd67c959e0d3524ffac1771dfbba87d2b6b4b4e99e42034a8b803f8b072'
    )

    @pytest.fixture
    def s3_request(self):
        from siilo.storages.amazon_s3 import _S3Request
        return _S3Request(
            method='PUT',
            endpoint='s3.amazonaws.com',
            bucket='examplebucket',
            key='test$file.text',
            headers={
                'Host': 'examplebucket.s3.amazonaws.com',
                'Date': 'Fri, 24 May 2013 00:00:00 GMT',
                'X-Amz-Date': '20130524T000000Z',
                'X-Amz-Storage-Class': 'REDUCED_REDUNDANCY',
                'X-Amz-Content-SHA256': (
                    '44ce7dd67c959e0d3524ffac1771dfbb'
                    'a87d2b6b4b4e99e42034a8b803f8b072'
                )
            },
            use_https=False,
        )


class TestSignerV4GETBucketLifecycleExample(_TestSignerV4Example):
    canonical_request = '''\
        GET
        /
        lifecycle=
        host:examplebucket.s3.amazonaws.com
        x-amz-content-sha256:\
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        x-amz-date:20130524T000000Z

        host;x-amz-content-sha256;x-amz-date
        e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

    string_to_sign = '''\
        AWS4-HMAC-SHA256
        20130524T000000Z
        20130524/us-east-1/s3/aws4_request
        9766c798316ff2757b517bc739a67f6213b4ab36dd5da2f94eaebf79c77395ca'''

    signature = (
        'fea454ca298b7da1c68078a5d1bdbfbbe0d65c699e0f91ac7a200a0136783543'
    )

    @pytest.fixture
    def s3_request(self):
        from siilo.storages.amazon_s3 import _S3Request
        return _S3Request(
            method='GET',
            use_https=False,
            endpoint='s3.amazonaws.com',
            bucket='examplebucket',
            key='',
            params={
                'lifecycle': '',
            },
            headers={
                'Host': 'examplebucket.s3.amazonaws.com',
                'X-Amz-Date': '20130524T000000Z',
                'X-Amz-Content-SHA256': (
                    'e3b0c44298fc1c149afbf4c8996fb924'
                    '27ae41e4649b934ca495991b7852b855'
                )
            }
        )


class TestSignerV4GETBucketListObjects(_TestSignerV4Example):
    canonical_request = '''\
        GET
        /
        max-keys=2&prefix=J
        host:examplebucket.s3.amazonaws.com
        x-amz-content-sha256:\
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        x-amz-date:20130524T000000Z

        host;x-amz-content-sha256;x-amz-date
        e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'''

    string_to_sign = '''\
        AWS4-HMAC-SHA256
        20130524T000000Z
        20130524/us-east-1/s3/aws4_request
        df57d21db20da04d7fa30298dd4488ba3a2b47ca3a489c74750e0f1e7df1b9b7'''

    signature = (
        '34b48302e7b5fa45bde8084f4b7868a86f0a534bc59db6670ed5711ef69dc6f7'
    )

    @pytest.fixture
    def s3_request(self):
        from siilo.storages.amazon_s3 import _S3Request
        return _S3Request(
            method='GET',
            use_https=False,
            endpoint='s3.amazonaws.com',
            bucket='examplebucket',
            key='',
            params={
                'max-keys': '2',
                'prefix': 'J',
            },
            headers={
                'Host': 'examplebucket.s3.amazonaws.com',
                'X-Amz-Date': '20130524T000000Z',
                'X-Amz-Content-SHA256': (
                    'e3b0c44298fc1c149afbf4c8996fb924'
                    '27ae41e4649b934ca495991b7852b855'
                )
            }
        )


class TestPresignerV4Example(object):
    @pytest.fixture(scope='class')
    def presigner(self, signer):
        from siilo.storages.amazon_s3 import _PresignerV4
        presigner = _PresignerV4(signer)
        presigner._get_timestamp = mock.Mock(return_value='20130524T000000Z')
        return presigner

    @pytest.fixture(scope='class')
    def s3_request(self, presigner):
        from siilo.storages.amazon_s3 import _S3Request
        request = _S3Request(
            method='GET',
            endpoint='s3.amazonaws.com',
            bucket='examplebucket',
            key='test.txt',
            use_https=True,
            use_path_style=False,
        )
        presigner.presign(request, expires=timedelta(hours=24))
        return request

    def test_scheme(self, s3_request):
        assert s3_request.scheme == 'https'

    def test_host(self, s3_request):
        assert s3_request.host == 'examplebucket.s3.amazonaws.com'

    def test_path(self, s3_request):
        assert s3_request.path == '/test.txt'

    def test_params(self, s3_request):
        assert s3_request.params == {
            'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
            'X-Amz-Credential': (
                'AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request'
            ),
            'X-Amz-Date': '20130524T000000Z',
            'X-Amz-Expires': '86400',
            'X-Amz-SignedHeaders': 'host',
            'X-Amz-Signature': (
                'aeeed9bbccd4d02ee5c0109b86d86835'
                'f995330da4c265957d157751f604d404'
            ),
        }


@pytest.mark.parametrize(
    ('input', 'output'),
    [
        (3600, 3600),
        (timedelta(days=1), 86400),
        (date(2014, 1, 5), 111600),
        (datetime(2014, 1, 5, 12, 0), 154800),
    ]
)
def test_expires_in_seconds(input, output):
    from siilo.storages.amazon_s3 import _expires_in_seconds
    with freezegun.freeze_time('2014-01-03 17:00'):
        assert _expires_in_seconds(input) == output


@pytest.mark.parametrize(
    ('string', 'quoted', 'encode_slash'),
    [
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', True),
        ('abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz', True),
        ('0123456789', '0123456789', True),
        ('-._~', '-._~', True),
        (' ', '%20', True),
        ('[]', '%5B%5D', True),
        ('/', '/', False),
        ('/', '%2F', True),
    ]
)
def test_uri_encode(string, quoted, encode_slash):
    from siilo.storages.amazon_s3 import _uri_encode
    assert _uri_encode(string, encode_slash) == quoted
