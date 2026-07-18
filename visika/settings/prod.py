from .base import *

# Production settings overrides
DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Database
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://user:pass@localhost:5432/db'),
}

# Caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Security Enhancements
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cloud Storage Configuration (Cloudinary)
# Only enable if CLOUDINARY_URL is provided
if env('CLOUDINARY_URL', default=None):
    INSTALLED_APPS.append('cloudinary')
    INSTALLED_APPS.append('cloudinary_storage')
    STORAGES["default"]["BACKEND"] = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Vercel Serverless File System is Read-Only except for /tmp (fallback)
    MEDIA_ROOT = '/tmp/media'

# Celery on Serverless
# Vercel doesn't support background Celery workers, so tasks must run synchronously
CELERY_TASK_ALWAYS_EAGER = True

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS Setup
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
CORS_ALLOW_CREDENTIALS = True
