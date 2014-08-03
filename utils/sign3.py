import argparse
import hashlib
import base64
import hmac


def parse_args():
    """Parse program arguments into an object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('key', help='Key to sign with')
    parser.add_argument('key_id', help='an ID of the key in use')
    return parser.parse_args()


def string_to_sign():
    return '\n'.join([
        '(request-target): get /packages/measures/',
        'accept: application/json',
        'date: Mon, 17 Feb 2014 06:11:05 GMT',
        'host: localhost:8000'])


def raw_sign(message, secret):
    """Sign a message."""
    digest = hmac.new(secret, message, hashlib.sha256).digest()
    return base64.b64encode(digest)


def http_signature(message, key_id, signature):
    """Return a tuple (message signature, HTTP header message signature)."""
    template = ('Signature keyId="%(keyId)s",algorithm="hmac-sha256",'
                'headers="%(headers)s",signature="%(signature)s"')
    headers = ['(request-target)', 'host', 'accept', 'date']
    return template % {
        'keyId': key_id,
        'signature': signature,
        'headers': ' '.join(headers),
    }


if __name__ == '__main__':
    args = parse_args()
    message = string_to_sign()
    signature = raw_sign(message, args.key)
    header = http_signature(message, args.key_id, signature)
    print "=== SIGNATURE ==="
    print signature
    print "=== HTTP HEADER SIGNATURE ==="
    print header
