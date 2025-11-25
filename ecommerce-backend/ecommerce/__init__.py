"""Initialize the Django project and set up the Celery application.

This module exposes the Celery app instance at import time so that
other modules can register tasks using ``ecommerce.celery.app``. The
presence of this import causes Celery to auto‑discover any ``tasks.py``
modules in installed apps.
"""

from .celery import app as celery_app  # noqa: F401

__all__ = ("celery_app",)