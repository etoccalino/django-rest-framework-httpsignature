from django.test import SimpleTestCase
# from django.contrib.auth import get_user_model
# User = get_user_model()
from rest_framework_httpsignature.authentication import SignatureAuthentication


class SignatureTestCase(SimpleTestCase):

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
