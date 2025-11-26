"""Custom middleware definitions.

This module contains middleware classes that provide additional
functionality to the request/response cycle. Middleware can be used
for logging, performance metrics, request manipulation, response
modification and more. The ``RequestTimingMiddleware`` below
measures the processing time of each request and adds the duration to
the response headers.
"""

import time
from typing import Callable, Any


class RequestTimingMiddleware:
    """Measure the duration of each HTTP request.

    This middleware records the time taken to process each request and
    attaches a custom header ``X-Request-Duration`` to the response. It
    can be extended to log request timing data to an external
    monitoring service.
    """

    def __init__(self, get_response: Callable[[Any], Any]) -> None:
        """Initialize the middleware with the next layer of the pipeline."""
        self.get_response = get_response

    def __call__(self, request):
        """Measure processing time and add it to the response."""
        start = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start
        # Attach the duration in milliseconds to the response headers
        response["X-Request-Duration"] = f"{duration * 1000:.2f}ms"
        return response