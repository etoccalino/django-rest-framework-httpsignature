from django.test import SimpleTestCase, RequestFactory
# from django.contrib.auth import get_user_model
# User = get_user_model()
from rest_framework_httpsignature.authentication import SignatureAuthentication
from rest_framework.exceptions import AuthenticationFailed


class HeadersUnitTestCase(SimpleTestCase):

    request = RequestFactory()
    ENDPOINT = '/api'

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
        req = self.request.get(self.ENDPOINT, {}, HTTP_X_DATE="some date")
        dict_to_sign = self.auth.build_dict_to_sign(req, ['date'])
        self.assertTrue('date' in dict_to_sign.keys())

    def test_build_signature_for_date_and_other(self):
        req = self.request.get(self.ENDPOINT, {}, HTTP_X_ACCEPT="*/*",
                               HTTP_X_DATE="some date")
        dict_to_sign = self.auth.build_dict_to_sign(req, ['accept', 'date'])
        self.assertTrue('date' in dict_to_sign.keys())
        self.assertTrue('accept' in dict_to_sign.keys())

    def test_build_signature_for_request_line(self):
        req = self.request.get(self.ENDPOINT, {}, HTTP_X_DATE="some date")
        dict_to_sign = self.auth.build_dict_to_sign(
            req,
            ['request-line', 'date'])
        self.assertTrue('date' in dict_to_sign.keys())
        self.assertTrue('request-line' not in dict_to_sign.keys())


class SignatureTestCase(SimpleTestCase):

    ENDPOINT = '/api'
    METHOD = 'GET'
    KEYID = 'some-key'
    SIGNATURE = 'some.signature'

    def setUp(self):
        self.auth = SignatureAuthentication()

    def build_signature(self, headers):
        template = ('Signature keyId="%(keyId)s",'
                    'headers="%(headers)s",signature="%(signature)s"')
        return template % {
            'keyId': self.KEYID,
            'headers': ' '.join(headers),
            'signature': self.SIGNATURE,
        }

    def test_no_headers_in_signature(self):
        signature = self.build_signature([])
        self.assertRaises(AuthenticationFailed,
                          self.auth.get_headers_from_signature, signature)

    def test_date_in_signature(self):
        signature = self.build_signature(['date'])
        headers = self.auth.get_headers_from_signature(signature)
        self.assertTrue('date' in headers)

    def test_many_in_signature(self):
        signature = self.build_signature(['date', 'accept', 'request-line'])
        headers = self.auth.get_headers_from_signature(signature)
        self.assertTrue('date' in headers)
        self.assertTrue('accept' in headers)
        self.assertTrue('request-line' in headers)
