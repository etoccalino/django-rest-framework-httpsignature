DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'rest_framework_httpsignature',
)

ROOT_URLCONF = 'rest_framework_httpsignature.tests'

SECRET_KEY = 'MY PRIVATE SECRET'
