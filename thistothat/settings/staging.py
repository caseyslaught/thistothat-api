import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

from thistothat.settings.base import *


DEBUG = True
STAGE = 'staging'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'data.staging.thistothat.io',
    'thistothat-staging.eba-qms9mvme.eu-central-1.elasticbeanstalk.com'
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ['THISTOTHAT_ELASTICACHE_URL']
    }
}

DATABASE_NAME = "thistothat_staging"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': os.environ['THISTOTHAT_MYSQL_USER'],
        'PASSWORD': os.environ['THISTOTHAT_MYSQL_PASSWORD'],
        'HOST': os.environ['THISTOTHAT_MYSQL_HOST'],
        'PORT': '3306',
    },
    'OPTIONS': {
        'charset': 'utf8mb4',
        'use_unicode': True,
    }
}

sentry_sdk.init(
    dsn=os.environ['THISTOTHAT_SENTRY_URL'],
    integrations=[DjangoIntegration()],
)
ignore_logger("django.security.DisallowedHost")

