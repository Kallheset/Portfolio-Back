"""
Development settings for Django project.

These settings are used for local development.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Database
# Use SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email backend - console for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug toolbar (if installed)
if "debug_toolbar" in INSTALLED_APPS:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Disable caching in development for easier debugging
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Logging - more verbose in development
LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["loggers"]["core"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# CORS settings for local development (if using separate frontend)
# CORS_ALLOW_ALL_ORIGINS = True  # Only for development!
