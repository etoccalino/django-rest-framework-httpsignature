===================================
django-rest-framework-httpsignature
===================================

.. image:: https://travis-ci.org/etoccalino/django-rest-framework-httpsignature.png?branch=master
           :target: https://travis-ci.org/etoccalino/django-rest-framework-httpsignature


Overview
========

Provides `HTTP Signature`_ support for `Django REST framework`_. The HTTP Signature package provides a way to achieve origin authentication and message integrity for HTTP messages. Similar to Amazon's `HTTP Signature scheme`_, used by many of its services. The `HTTP Signature`_ specification is currently an IETF draft.


.. contents::

Installation
============

Installing the package via the repository::

   pip install djangorestframework-httpsignature

The current implementation depends on `http_signature by David Lehn`_, who has updated the original code to match the revised spec. This dependency is reflected in the ``REQUIREMENTS.txt`` file, and pip will pull the code from David's repository.


Running the tests
=================

To run the tests for the packages, use the following command on the repository root directory::

  python manage.py test

Usage
=====

To authenticate HTTP requests via HTTP signature, you need to:

1. Install this package in your Django project, as instructed in `Installation`_.
2. Add ``rest_framework_httpsignature`` to your ``settings.py`` INSTALLED_APPS.
3. In your app code, extend the ``SignatureAuthentication`` class, as follows::

    # my_api/auth.py

    from rest_framework_httpsignature.authentication import SignatureAuthentication

    class MyAPISignatureAuthentication(SignatureAuthentication):
        # The HTTP header used to pass the consumer key ID.
        # Defaults to 'X-Api-Key'.
        API_KEY_HEADER = 'X-Api-Key'

        # A method to fetch (User instance, user_secret_string) from the
        # consumer key ID, or None in case it is not found.
        def fetch_user_data(self, api_key):
            # ...
            # example implementation:
            try:
                user = User.objects.get(api_key=api_key)
                return (user, user.secret)
            except User.DoesNotExist:
                return None


4. Configure Django REST framework to use you authentication class; e.g.::

    # my_project/settings.py

    # ...
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
           'my_api.auth.MyAPISignatureAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }
    # The above will force HTTP signature for all requests.
    # ...


Roadmap
=======

- Currently, the library only support HMAC SHA256 for signing.
- The ``REQUIREMENTS.txt`` file is fairly strict. It is very possible that previous versions of Django and Django REST framework are supported.
- Since HTTP Signature uses a HTTP header for the request date and time, the authentication class could deal with request expiry.


Example usage & session w/cURL
==============================

Assuming the setup detailed in `Usage`_, a project running on ``localhost:8000`` could be probed with cURL as follows::

  ~$ SSS=Base64(Hmac(SECRET, "Date: Mon, 17 Feb 2014 06:11:05 GMT", SHA256))
  ~$ curl -v -H 'Date: "Mon, 17 Feb 2014 06:11:05 GMT"' -H 'Authorization: Signature keyId="my-key",algorithm="hmac-sha256",headers="date",signature="SSS"'

And with much less pain, using the modules ``requests`` and ``http_signature``::

  import requests
  from http_signature.requests_auth import HTTPSignatureAuth

  API_KEY_ID = 'su-key'
  SECRET = 'my secret string'

  signature_headers = ['request-line', 'accept', 'date', 'host']
  headers = {
      'Host': 'localhost:8000',
      'Accept': 'application/json',
      'X-Api-Key': API_KEY_ID,
  }

  # We omit the "Date" header, so http_signature adds it.
  auth = HTTPSignatureAuth(key_id=API_KEY_ID, secret=SECRET,
                           algorithm='hmac-sha256',
                           headers=signature_headers)
  req = requests.get('http://localhost:8000/resource/',
                     auth=auth, headers=headers)
  print req.content


.. References:
.. _`HTTP Signature`: https://datatracker.ietf.org/doc/draft-cavage-http-signatures/
.. _`Django REST framework`: http://django-rest-framework.org/
.. _`HTTP Signature scheme`: http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
.. _`http_signature by David Lehn`: https://github.com/digitalbazaar/py-http-signature
