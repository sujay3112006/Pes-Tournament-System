"""
Football Tournament Backend - Core Module
"""

# Celery app initialization
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Celery is optional for development
    pass

default_app_config = 'core.apps.CoreConfig'
