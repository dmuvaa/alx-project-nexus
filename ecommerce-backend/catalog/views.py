"""ViewSets for products, categories and variations with advanced features.

The catalog views expose CRUD operations for categories, products and
their variations. Custom permission classes restrict modification to
administrators while allowing read‑only access to authenticated users.
Additional filtering, searching and ordering are provided for products,
along with optional queryset annotations for discounted prices and
inventory value.
"""

from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, ProductVariation
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer
from .filters import ProductFilter


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow unrestricted read access but restrict modification to admins."""

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD operations for categories with admin permissions."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD operations for products with filtering and ordering support."""

    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "brand"]
    ordering_fields = ["price", "created_at", "quantity"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Optionally annotate the queryset with computed fields based on query params."""
        qs = super().get_queryset()
        request = self.request
        discount = request.query_params.get("discount")
        annotate_stock = request.query_params.get("stock_value")
        if discount:
            try:
                discount_val = float(discount)
                qs = qs.with_discounted_price(discount_val)
            except ValueError:
                pass
        if annotate_stock is not None:
            qs = qs.with_stock_value()
        return qs


class ProductVariationViewSet(viewsets.ModelViewSet):
    """CRUD operations for product variations.

    Variations are managed per product. Only administrators may create,
    update or delete variations; all authenticated users may list and
    retrieve them. Filtering by product id can be performed via a
    query parameter ``product``.
    """

    queryset = ProductVariation.objects.select_related("product").all()
    serializer_class = ProductVariationSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["product_id", "name", "value"]
    search_fields = ["name", "value", "sku"]
    ordering_fields = ["price", "quantity"]
    ordering = ["product_id", "name"]