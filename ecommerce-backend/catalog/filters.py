"""Filter definitions for catalog views.

Filters provide advanced querying capabilities on the catalog API. They
allow clients to restrict results based on numeric ranges, boolean
flags and foreign key relationships. These definitions are applied in
the ``ProductViewSet`` via DjangoFilterBackend.
"""

import django_filters.rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    """Provide advanced filtering options for the product list."""

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.NumberFilter(field_name="category_id", lookup_expr="exact")

    class Meta:
        model = Product
        fields = ["category", "in_stock", "min_price", "max_price"]