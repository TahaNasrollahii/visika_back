from .base import *

# Local development settings overrides
DEBUG = True
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=["127.0.0.1", "localhost"])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"), 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CORS_ALLOW_ALL_ORIGINS = True

# Overwrite log format to be simpler for dev
LOGGING['handlers']['console']['formatter'] = 'verbose'
