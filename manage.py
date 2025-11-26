#!/usr/bin/env python
"""Django's command‑line utility for administrative tasks.

This script serves as the entry point for most management commands used
to interact with the Django project. It sets the default settings
module and delegates execution to Django's built‑in command
infrastructure. Keeping this file minimal avoids import side effects
when running commands such as migrations or the development server.
"""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    # If the DJANGO_SETTINGS_MODULE environment variable isn't set,
    # default to the settings module for this project. This allows
    # commands to be executed without needing to export variables in
    # development environments.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()