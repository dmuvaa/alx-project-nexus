"""URL configuration for the e‑commerce project.

This module defines the top level URL routes for the project. API
endpoints are organized by application and exposed under the ``/api/``
prefix. A schema endpoint and Swagger UI are also provided for API
exploration. To extend the API surface, include additional URL
configurations from new apps here.
"""

# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from django.http import JsonResponse


# def api_root(request):
#     """
#     Simple API root that shows a status message and useful endpoints.
#     """
#     return JsonResponse(
#         {
#             "message": "E-commerce API is running",
#             "endpoints": {
#                 "users": "/api/users/",
#                 "catalog": "/api/catalog/",
#                 "orders": "/api/orders/",
#                 "payments": "/api/payments/",
#                 "schema": "/api/schema/",
#                 "docs": "/api/docs/",
#                 "admin": "/admin/",
#             }
#         }
#     )


# urlpatterns = [
#     path("", api_root, name="root"),
#     path("admin/", admin.site.urls),
#     path("api/users/", include("users.urls")),
#     path("api/catalog/", include("catalog.urls")),
#     path("api/payments/", include("payments.urls")),
#     path("api/orders/", include("orders.urls")),
#     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
#     path(
#         "api/docs/",
#         SpectacularSwaggerView.as_view(url_name="schema"),
#         name="swagger-ui",
#     ),
# ]

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse


def api_root(request):
    """
    API root that shows status and full endpoint URLs.
    """

    def full(path: str) -> str:
        # Builds an absolute URL like https://your-domain.com/api/...
        return request.build_absolute_uri(path)

    return JsonResponse(
        {
            "message": "E-commerce API is running",
            "endpoints": {
                "users": full("/api/users/"),
                "catalog": full("/api/catalog/"),
                "orders": full("/api/orders/"),
                "payments": full("/api/payments/"),
                "schema": full("/api/schema/"),
                "docs": full("/api/docs/"),
                "admin": full("/admin/"),
            },
        }
    )


urlpatterns = [
    path("", api_root, name="root"),
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/catalog/", include("catalog.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
