from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': get_env_variable("POSTGRES_USER"),
        'PASSWORD': get_env_variable("POSTGRES_PASSWORD"),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
