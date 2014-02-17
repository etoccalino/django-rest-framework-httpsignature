from setuptools import setup


setup(
    name='djangorestframework-httpsignature',
    version='0.1.0',
    url='https://github.com/etoccalino/django-rest-framework-httpsignature',
    license='MIT',
    description='HTTP Signature support for Django REST framework',
    install_requires=open('REQUIREMENTS.txt').read().split('\n'),
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
