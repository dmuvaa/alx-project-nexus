"""Custom context managers for common patterns.

Context managers encapsulate common setup and teardown logic, ensuring
resources are properly managed. This module defines context managers
used throughout the project, such as database atomic operations with
timing and temporary environment variable overrides.
"""

import os
import time
from contextlib import contextmanager
from typing import Iterator, Dict, Any

from django.db import transaction


@contextmanager
def atomic_transaction_with_logging() -> Iterator[None]:
    """Wrap a block in a database transaction and log its duration.

    This context manager provides a convenient way to execute a series of
    database operations atomically while measuring how long the operations
    take. The timing information is printed to stdout but could be
    redirected to a logging framework as needed.
    """
    start = time.perf_counter()
    with transaction.atomic():
        yield
    duration = time.perf_counter() - start
    print(f"Atomic transaction executed in {duration:.4f} seconds")


@contextmanager
def temporary_env(env_vars: Dict[str, str]) -> Iterator[None]:
    """Temporarily set environment variables within a context.

    Environment variables specified in ``env_vars`` will be applied when
    entering the context and restored to their original values upon exit.

    Args:
        env_vars: A dictionary mapping environment variable names to
            temporary values.
    """
    original: Dict[str, Any] = {}
    try:
        for key, value in env_vars.items():
            original[key] = os.environ.get(key)
            os.environ[key] = value
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value