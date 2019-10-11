from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASS"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=60)
