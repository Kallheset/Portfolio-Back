"""
Production settings for Django project.

These settings are used for production deployment.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Session and CSRF security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"

# Database - Override with PostgreSQL in production
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PASSWORD'),
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env('DB_PORT', default='5432'),
#         'CONN_MAX_AGE': 600,
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#     }
# }

# Email backend - use SMTP in production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Static files - use WhiteNoise or cloud storage
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Cache - use Redis in production
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'SOCKET_CONNECT_TIMEOUT': 5,
#             'SOCKET_TIMEOUT': 5,
#             'RETRY_ON_TIMEOUT': True,
#             'MAX_CONNECTIONS': 50,
#             'CONNECTION_POOL_KWARGS': {
#                 'max_connections': 50,
#                 'retry_on_timeout': True,
#             },
#         },
#         'KEY_PREFIX': 'portfolio',
#     }
# }

# Logging - send errors to admins
ADMINS = [
    (env("ADMIN_NAME", default="Admin"), env("ADMIN_EMAIL", default="admin@example.com")),
]

LOGGING["handlers"]["mail_admins"] = {
    "level": "ERROR",
    "class": "django.utils.log.AdminEmailHandler",
    "filters": ["require_debug_false"],
}

LOGGING["loggers"]["django.request"]["handlers"].append("mail_admins")

# Content Security Policy
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
# CSP_IMG_SRC = ("'self'", "data:", "https:")
# CSP_FONT_SRC = ("'self'", "cdn.jsdelivr.net")
