
from thistothat.settings.base import *


COGNITO_APP_ID = ""
COGNITO_USER_POOL_ID = ""

ALLOWED_HOSTS = ['*']
DEBUG = True
STAGE = 'development'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/thistothat_cache',
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



