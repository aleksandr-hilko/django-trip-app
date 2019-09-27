from .base import *

INSTALLED_APPS += ("debug_toolbar",)

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)

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
