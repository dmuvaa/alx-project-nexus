"""Serializers for categories, products and variations.

Serializers convert complex types such as Django models into native
Python datatypes that can then be rendered into JSON, XML or other
content types. They also provide deserialization, allowing parsed
data to be converted back into complex types after validation.
"""

from rest_framework import serializers

from .models import Category, Product, ProductVariation


class CategorySerializer(serializers.ModelSerializer):
    """Serialize category objects for API representation."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent"]


class ProductVariationSerializer(serializers.ModelSerializer):
    """Serialize product variation objects for nested representation."""

    class Meta:
        model = ProductVariation
        fields = [
            "id",
            "name",
            "value",
            "sku",
            "price",
            "quantity",
            "in_stock",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serialize product objects including optional computed fields and variations."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    variations = ProductVariationSerializer(many=True, read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    stock_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "sku",
            "brand",
            "price",
            "quantity",
            "in_stock",
            "category",
            "category_id",
            "created_at",
            "updated_at",
            "variations",
            "discounted_price",
            "stock_value",
        ]