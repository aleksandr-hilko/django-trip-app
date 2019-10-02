from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable("DB_NAME"),
        'USER': get_env_variable("DB_USER"),
        'PASSWORD': get_env_variable("DB_PASS"),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
