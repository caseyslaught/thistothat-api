
from thistothat.settings.base import *


ALLOWED_HOSTS = ['*']
DEBUG = True
STAGE = 'development'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASE_NAME = "thistothat_development"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': os.environ['LOCAL_MYSQL_USER'],
        'PASSWORD': os.environ['LOCAL_MYSQL_PASSWORD'],
        'HOST': os.environ['LOCAL_MYSQL_HOST'],
        'PORT': '3306',
    },
    'OPTIONS': {
        'charset': 'utf8mb4',
        'use_unicode': True,
    }
}



