#!/usr/bin/env python
"""Django's command‑line utility for administrative tasks.

This script serves as the entry point for most management commands used
to interact with the Django project. It ensures that the Django
``ecommerce`` project package is importable even when this file lives
outside of the project package (for example in the repository root).

The script inserts the ``ecommerce-backend`` directory into
``sys.path`` so Python can locate the ``ecommerce`` package. It then
delegates to Django's built‑in command infrastructure. Keeping this
file minimal avoids import side effects when running commands such as
migrations or the development server.
"""

import os
import sys
from pathlib import Path


def main() -> None:
    """Run administrative tasks."""
    # Ensure the Django project package is on the Python path.  The
    # ``ecommerce`` package lives in the ``ecommerce-backend`` directory.
    base_dir = Path(__file__).resolve().parent
    backend_dir = base_dir / "ecommerce-backend"
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    # Configure the default settings module for this project.  If
    # DJANGO_SETTINGS_MODULE is already defined in the environment
    # (e.g. when running under uWSGI or Gunicorn), this call is a
    # no-op.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()