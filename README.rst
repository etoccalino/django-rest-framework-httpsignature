===================================
django-rest-framework-httpsignature
===================================

.. image:: https://travis-ci.org/etoccalino/django-rest-framework-httpsignature.png?branch=master
           :target: https://travis-ci.org/etoccalino/django-rest-framework-httpsignature


Overview
--------

Provides `HTTP Signature`_ support for `Django REST framework`_. The HTTP Signature package provides a way to achieve origin authentication and message integrity for HTTP messages. Similar to Amazon's `HTTP Signature scheme`_, used by many of its services. The `HTTP Signature`_ specification is currently an IETF draft.


Installation
------------

Installing the package via the repository::

   pip install git+https://github.com/etoccalino/django-rest-framework-httpsignature

The current implementation depends on `http_signature by David Lehn`_, who has updated the original code to match the revised spec. This dependency is reflected in the `REQUIREMENTS.txt` file, and pip will pull the code from David's repository.


Running the tests
-----------------

To run the tests for the packages, use the following command on the repository root directory::

  python manage.py test rest_framework_httpsignature

Usage
-----

TODO:

- Extend and complete SingatureAuthentication.
- Configure REST_FRAMEWORK in settings.py


Limitations
-----------

TODO:

- document support for HMAC-SHA256 only.
- document lack of requirements version investigation.


Example usage & session w/cURL
------------------------------

TODO:

- extending SignatureAuthentication for in-memory api key data store.
- edit setting.py to require authentication.
- using cURL to hit a URL.


.. References:
.. _`HTTP Signature`: https://datatracker.ietf.org/doc/draft-cavage-http-signatures/
.. _`Django REST framework`: http://django-rest-framework.org/
.. _`HTTP Signature scheme`: http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
.. _`http_signature by David Lehn`: https://github.com/digitalbazaar/py-http-signature
