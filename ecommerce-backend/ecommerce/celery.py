"""Celery application configuration for the e‑commerce project.

This module defines and configures the Celery application used for
running asynchronous tasks and periodic jobs. Configuration values are
drawn from the Django settings module so that the broker and result
backends can be customized via environment variables. The app is
automatically discovered by importing this module in ``ecommerce/__init__.py``.
"""

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

"""Instantiate the Celery application. The name here should match the Django project directory name so that Celery can discover tasks correctly."""
app = Celery("ecommerce")

"""Configure Celery to use Django's settings module. Any configuration keys prefixed with ``CELERY_`` in settings will be picked up automatically. 
For example, ``CELERY_BROKER_URL`` specifies the message broker and ``CELERY_RESULT_BACKEND`` specifies where results should be stored."""
app.config_from_object("django.conf:settings", namespace="CELERY")

"""Load task modules from all installed Django apps. Celery will look
for a ``tasks.py`` module in each app listed in INSTALLED_APPS."""
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self) -> None:
    """A simple task for debugging purposes.

    This task prints its request information to help ensure Celery is
    configured correctly. It can be invoked from the command line with
    ``celery -A ecommerce debug_task.delay()``.
    """
    print(f"Request: {self.request!r}")