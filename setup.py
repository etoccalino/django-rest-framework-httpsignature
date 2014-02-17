from setuptools import setup


setup(
    name='djangorestframework-httpsignature',
    version='0.1.0',
    url='https://github.com/etoccalino/django-rest-framework-httpsignature',

    license='LICENSE.txt',
    description='HTTP Signature support for Django REST framework',
    long_description=open('README.txt').read(),

    install_requires=[
        'Django==1.6.2',
        'djangorestframework==2.3.12',
        'pycrypto==2.6.1',
        'http_signature'
    ],
    dependency_links=[
        'https://github.com/etoccalino/py-http-signature/archive/v0.2.0.zip#egg=http_signature-0.2.0',
    ],

    author='Elvio Toccalino',
    author_email='me@etoccalino.com',
    packages=['rest_framework_httpsignature'],
    # package_data={
    #     'rest_framework_httpsignature': ,
    # },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
