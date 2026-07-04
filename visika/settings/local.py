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
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

CORS_ALLOW_ALL_ORIGINS = True

# Run Celery tasks synchronously in local dev to avoid requiring Redis
CELERY_TASK_ALWAYS_EAGER = True

# Overwrite log format to be simpler for dev
LOGGING['handlers']['console']['formatter'] = 'verbose'
