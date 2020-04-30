
from thistothat.settings.base import *


ALLOWED_HOSTS = ['*']
DEBUG = True
STAGE = 'testing'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASE_NAME = "thistothat_testing.db"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_NAME
    }
}


