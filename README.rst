===================================
django-rest-framework-httpsignature
===================================

TODO:

- Travis tag


Overview
--------

Provides `HTTP Signature`_ support for `Django REST framework`_. The HTTP Signature provides a way to achieve origin authentication and message integrity to HTTP messages.

TODO:

- Mention Amazon `HTTP Signature scheme`_, and mention main differences.


Installation
------------

Installing the package via the repository::

   pip install git+https://github.com/etoccalino/django-rest-framework-httpsignature

TODO:

- document requirement of `http_signature by David Lehn`_ and motivation (update to version 01 of spec).


Running the tests
-----------------

To run the tests for the packages, su::

  python manage.py test rest_framework_httpsignature

Usage
-----

TODO:

- Extend and complete SingatureAuthentication.
- Configure REST_FRAMEWORK in settings.py


Example usage & session w/cURL
------------------------------

TODO:

- extending SignatureAuthentication for in-memory api key data store.
- edit setting.py to require authentication.
- using cURL to hit a URL.


.. References:
.. _`HTTP Signature`: http://tools.ietf.org/html/draft-cavage-http-signatures-01/
.. _`Django REST framework`: http://django-rest-framework.org/
.. _`HTTP Signature scheme`: http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
.. _`http_signature by David Lehn`: https://github.com/digitalbazaar/py-http-signature
