from django.test import SimpleTestCase, TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework_httpsignature.authentication import SignatureAuthentication
from rest_framework.exceptions import AuthenticationFailed
import re

User = get_user_model()

ENDPOINT = '/api'
METHOD = 'GET'
KEYID = 'some-key'
SECRET = 'my secret string'
SIGNATURE = 'some.signature'


def build_signature(headers, key_id=KEYID, signature=SIGNATURE):
    """Build a signature string."""
    template = ('Signature keyId="%(keyId)s",algorithm="hmac-sha256",'
                'headers="%(headers)s",signature="%(signature)s"')
    return template % {
        'keyId': key_id,
        'signature': signature,
        'headers': ' '.join(headers),
    }


class HeadersUnitTestCase(SimpleTestCase):

    request = RequestFactory()

    def setUp(self):
        self.auth = SignatureAuthentication()

    def test_special_header_names(self):
        for special in ['Content-Type', 'CONTENT-TYPE', 'content-type']:
            canon = self.auth.header_canonical(special)
            self.assertEqual('CONTENT-TYPE', canon)

        for special in ['Content-Length', 'CONTENT-LENGTH', 'content-length']:
            canon = self.auth.header_canonical(special)
            self.assertEqual('CONTENT-LENGTH', canon)

    def test_header_names(self):
        headers = ['X-Api-Key', 'Authentication', 'date', 'X-Something-Else']
        for header in headers:
            canon = self.auth.header_canonical(header)
            expected = 'HTTP_%s' % header.upper().replace('-', '_')
            self.assertEqual(expected, canon)

    def test_build_signature_for_date(self):
        req = self.request.get(ENDPOINT, {}, HTTP_X_DATE="some date")
        dict_to_sign = self.auth.build_dict_to_sign(req, ['date'])
        self.assertTrue('date' in dict_to_sign.keys())

    def test_build_signature_for_date_and_other(self):
        req = self.request.get(ENDPOINT, {}, HTTP_X_ACCEPT="*/*",
                               HTTP_X_DATE="some date")
        dict_to_sign = self.auth.build_dict_to_sign(req, ['accept', 'date'])
        self.assertTrue('date' in dict_to_sign.keys())
        self.assertTrue('accept' in dict_to_sign.keys())

    def test_build_signature_for_request_line(self):
        req = self.request.get(ENDPOINT, {}, HTTP_X_DATE="some date")
        dict_to_sign = self.auth.build_dict_to_sign(
            req,
            ['request-line', 'date'])
        self.assertTrue('date' in dict_to_sign.keys())
        self.assertTrue('request-line' not in dict_to_sign.keys())


class SignatureTestCase(SimpleTestCase):

    def setUp(self):
        self.auth = SignatureAuthentication()

    def test_no_headers_in_signature(self):
        signature = build_signature([])
        self.assertRaises(AuthenticationFailed,
                          self.auth.get_headers_from_signature, signature)

    def test_date_in_signature(self):
        signature = build_signature(['date'])
        headers = self.auth.get_headers_from_signature(signature)
        self.assertTrue('date' in headers)

    def test_many_in_signature(self):
        signature = build_signature(['date', 'accept', 'request-line'])
        headers = self.auth.get_headers_from_signature(signature)
        self.assertTrue('date' in headers)
        self.assertTrue('accept' in headers)
        self.assertTrue('request-line' in headers)

    def test_get_signature(self):
        signature_string = build_signature(['request-line', 'date'])
        signature = self.auth.get_signature_from_signature_string(
            signature_string)
        self.assertEqual(SIGNATURE, signature)

    def test_get_signature_without_headers(self):
        signature_string = build_signature([])
        signature = self.auth.get_signature_from_signature_string(
            signature_string)
        self.assertEqual(SIGNATURE, signature)


class BuildSignatureTestCase(SimpleTestCase):

    request = RequestFactory()
    KEYID = 'su-key'

    def setUp(self):
        self.auth = SignatureAuthentication()

    def test_build_signature(self):
        # TO SIGN:
        #
        # GET /packages/measures/ HTTP/1.1
        # accept: application/json
        # date: Mon, 17 Feb 2014 06:11:05 GMT
        # host: localhost:8000

        headers = ['request-line', 'accept', 'date', 'host']
        expected_signature = 'DvQs08T31vR83r5tUqonb6EcpHb+BtDPEbCZ1/WVH58='
        expected_signature_string = build_signature(
            headers,
            key_id=self.KEYID,
            signature=expected_signature)

        req = RequestFactory().get(
            '/packages/measures/', {},
            HTTP_HOST='localhost:8000',
            HTTP_DATE='Mon, 17 Feb 2014 06:11:05 GMT',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION=expected_signature_string)

        signature_string = self.auth.build_signature(
            self.KEYID, SECRET, req)
        signature = re.match(
            '.*signature="(.+)",?.*', signature_string).group(1)
        self.assertEqual(expected_signature, signature)


class SignatureAuthenticationTestCase(TestCase):

    class APISignatureAuthentication(SignatureAuthentication):
        """Extend the SignatureAuthentication to test it."""

        API_KEY_HEADER = 'X-Api-Key'

        def __init__(self, user):
            self.user = user

        def fetch_user_data(self, api_key):
            if api_key != KEYID:
                return None

            return (self.user, SECRET)

    TEST_USERNAME = 'test-user'
    TEST_PASSWORD = 'test-password'

    def setUp(self):
        self.test_user = User(username=self.TEST_USERNAME)
        self.test_user.set_password(self.TEST_PASSWORD)
        self.auth = self.APISignatureAuthentication(self.test_user)

    def test_no_credentials(self):
        request = RequestFactory().get(ENDPOINT)
        res = self.auth.authenticate(request)
        self.assertIsNone(res)

    def test_only_api_key(self):
        request = RequestFactory().get(
            ENDPOINT, {},
            HTTP_X_API_KEY=KEYID)
        self.assertRaises(AuthenticationFailed,
                          self.auth.authenticate, request)

    def test_bad_signature(self):
        request = RequestFactory().get(
            ENDPOINT, {},
            HTTP_X_API_KEY=KEYID,
            HTTP_AUTHORIZATION='some-wrong-value')
        self.assertRaises(AuthenticationFailed,
                          self.auth.authenticate, request)

    def test_can_authenticate(self):
        headers = ['request-line', 'accept', 'date', 'host']
        expected_signature = 'DvQs08T31vR83r5tUqonb6EcpHb+BtDPEbCZ1/WVH58='
        expected_signature_string = build_signature(
            headers,
            key_id=KEYID,
            signature=expected_signature)
        request = RequestFactory().get(
            '/packages/measures/', {},
            HTTP_HOST='localhost:8000',
            HTTP_DATE='Mon, 17 Feb 2014 06:11:05 GMT',
            HTTP_ACCEPT='application/json',
            HTTP_AUTHORIZATION=expected_signature_string,
            HTTP_X_API_KEY=KEYID)

        result = self.auth.authenticate(request)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], self.test_user)
        self.assertEqual(result[1], KEYID)
