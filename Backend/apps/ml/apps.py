"""ML App Configuration"""
from django.apps import AppConfig


class MLConfig(AppConfig):
    """ML app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ml'
    verbose_name = 'Machine Learning'
