"""Database models for the catalog app.

This module defines the models representing product categories,
products and product variations. A custom queryset on ``Product``
provides convenient methods for advanced queries such as computing
discounted prices and inventory value. The models are designed to
support hierarchical categories, products with optional variations and
stock management.
"""

from django.db import models
from django.db.models import F, FloatField, Value
from django.db.models.functions import Coalesce


class Category(models.Model):
    """Represents a logical grouping of products with optional hierarchy.

    Categories can be nested to form a tree. For example, ``Electronics`` may
    be the parent of ``TVs`` and ``Speakers``. A self‑referential foreign
    key defines the parent category. If ``parent`` is ``None`` then the
    category is a top‑level category. Indexes on ``name`` and ``slug``
    accelerate lookups by these fields.
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        help_text="Optional parent category for hierarchical organization",
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        """Return a user‑friendly representation of the category."""
        return self.name


class ProductQuerySet(models.QuerySet):
    """Custom queryset providing advanced query operations."""

    def with_discounted_price(self, discount: float) -> "ProductQuerySet":
        """Annotate products with a discounted price.

        Args:
            discount: A decimal percentage discount to apply, e.g. 0.1 for 10%.

        Returns:
            A queryset annotated with a ``discounted_price`` field.
        """
        return self.annotate(discounted_price=F("price") * (1 - discount))

    def with_stock_value(self) -> "ProductQuerySet":
        """Annotate products with their total inventory value.

        The ``stock_value`` is computed as ``price * quantity``. If
        ``quantity`` is null, it is treated as zero using ``Coalesce``.
        """
        return self.annotate(
            stock_value=F("price") * Coalesce(F("quantity"), Value(0))
        )


class Product(models.Model):
    """Represents a sellable item in the catalog.

    Each product belongs to a category and may have one or more
    variations (e.g., different colors or sizes). Additional fields
    capture commonly used product attributes such as SKU and brand. A
    product's stock quantity reflects the number of items available
    across all variations when no variations exist. When variations
    exist, their quantities are summed in business logic to determine
    availability.
    """

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT,
        db_index=True,
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    description = models.TextField(blank=True)
    sku = models.CharField(
        max_length=100,
        blank=True,
        help_text="Stock Keeping Unit identifier for this product",
    )
    brand = models.CharField(
        max_length=100,
        blank=True,
        help_text="Brand or manufacturer of the product",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    quantity = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Available stock when the product has no variations",
    )
    in_stock = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Attach the custom manager that provides advanced query methods
    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["in_stock", "price"]),
            models.Index(fields=["category", "price"]),
        ]

    def __str__(self) -> str:
        """Return the product's name as its string representation."""
        return self.name


class ProductVariation(models.Model):
    """Represents a specific variation of a product.

    Variations capture attributes that differentiate individual SKUs of
    the same product, such as color, size or finish. Each variation
    maintains its own SKU, price and quantity. When all variations are
    depleted, the parent product is considered out of stock. Unique
    constraints prevent duplicate attribute combinations for the same
    product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations",
    )
    name = models.CharField(
        max_length=50,
        help_text="Name of the attribute (e.g., 'Color', 'Size')",
    )
    value = models.CharField(
        max_length=50,
        help_text="Value of the attribute (e.g., 'Red', 'XL')",
    )
    sku = models.CharField(
        max_length=100,
        blank=True,
        help_text="Unique SKU for this specific variation",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Override base price for this variation",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Stock quantity available for this variation",
    )
    in_stock = models.BooleanField(
        default=True,
        help_text="Whether the variation is currently available",
    )

    class Meta:
        unique_together = ("product", "name", "value")
        ordering = ["product", "name", "value"]

    def __str__(self) -> str:
        """Return a human‑readable representation of the variation."""
        return f"{self.product.name} - {self.name}: {self.value}"