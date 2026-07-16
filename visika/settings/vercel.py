from .base import *
import os

# Vercel/Production settings
DEBUG = False

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-for-build')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database - Neon Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE', ''),
        'USER': os.environ.get('PGUSER', ''),
        'PASSWORD': os.environ.get('PGPASSWORD', ''),
        'HOST': os.environ.get('PGHOST', ''),
        'PORT': os.environ.get('PGPORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Alternatively, use DATABASE_URL format:
# DATABASES = {
#     'default': env.db('DATABASE_URL', default='postgres://user:pass@localhost:5432/db'),
# }

# Redis/Cache - Upstash
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
    }
}

# CORS - Allow Vercel frontend
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True

# CSRF - Allow Vercel frontend
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# SSL/HTTPS (Vercel handles SSL termination)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Vercel handles this
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'

# Static files - WhiteNoise for serverless
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files - Use Cloudflare R2 or S3 when configured
# For now, media will not persist in serverless (use R2 for production)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Disable HSTS in favor of Vercel's SSL
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Celery - Use Upstash or skip for now
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', '')

# If no Redis for Celery, run tasks synchronously
if not CELERY_BROKER_URL:
    CELERY_TASK_ALWAYS_EAGER = True
