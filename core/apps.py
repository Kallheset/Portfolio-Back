"""Django app configuration for core application."""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration class for the core portfolio app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
