from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable("DB_NAME"),
        'USER': get_env_variable("DB_USER"),
        'PASSWORD': get_env_variable("DB_PASS"),
        'HOST': 'db',
        'PORT': 5432,
    }
}
