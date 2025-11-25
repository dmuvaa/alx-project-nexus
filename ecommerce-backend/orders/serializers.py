"""Serializers for shopping carts, orders and shipments."""

from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from catalog.serializers import ProductSerializer, ProductVariationSerializer
from .models import Cart, CartItem, Order, OrderItem, Shipment


class CartItemSerializer(serializers.ModelSerializer):
    """Serialize a single cart item."""

    product = ProductSerializer(read_only=True)
    variation = ProductVariationSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem._meta.get_field("product").remote_field.model.objects.all(),
        source="product",
        write_only=True,
    )
    variation_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem._meta.get_field("variation").remote_field.model.objects.all(),
        source="variation",
        allow_null=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "product",
            "product_id",
            "variation",
            "variation_id",
            "quantity",
            "price",
        ]
        read_only_fields = ["id", "cart", "product", "variation", "price"]


class CartSerializer(serializers.ModelSerializer):
    """Serialize a shopping cart with its items."""

    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "checked_out",
            "items",
            "total",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at", "checked_out", "items", "total"]

    def get_total(self, obj: Cart) -> Decimal:
        """Calculate the total cost of all items in the cart."""
        return sum((item.price * item.quantity for item in obj.items.all()), Decimal("0"))


class AddCartItemSerializer(serializers.Serializer):
    """Serializer for adding a new item to the cart."""

    product_id = serializers.IntegerField()
    variation_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        """Ensure the product/variation exists and determine the price."""
        from catalog.models import Product, ProductVariation
        product_id = attrs.get("product_id")
        variation_id = attrs.get("variation_id")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Invalid product ID."})
        variation = None
        if variation_id:
            try:
                variation = ProductVariation.objects.get(pk=variation_id, product=product)
            except ProductVariation.DoesNotExist:
                raise serializers.ValidationError({"variation_id": "Invalid variation for this product."})
        attrs["product_obj"] = product
        attrs["variation_obj"] = variation
        attrs["unit_price"] = variation.price if variation else product.price
        return attrs

    def save(self, **kwargs) -> CartItem:
        """Add or update the cart item for the given product/variation."""
        cart: Cart = self.context["cart"]
        product: Product = self.validated_data["product_obj"]
        variation: ProductVariation = self.validated_data.get("variation_obj")
        quantity: int = self.validated_data["quantity"]
        unit_price: Decimal = self.validated_data["unit_price"]
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, variation=variation,
            defaults={"quantity": quantity, "price": unit_price},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
        return item


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating the quantity of an existing cart item."""

    quantity = serializers.IntegerField(min_value=1)

    def update(self, instance: CartItem, validated_data):
        instance.quantity = validated_data["quantity"]
        instance.save(update_fields=["quantity"])
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    """Serialize an item within an order."""

    product = ProductSerializer(read_only=True)
    variation = ProductVariationSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "variation",
            "quantity",
            "price",
        ]


class ShipmentSerializer(serializers.ModelSerializer):
    """Serialize shipment details for an order."""

    class Meta:
        model = Shipment
        fields = [
            "tracking_number",
            "carrier",
            "status",
            "shipped_at",
            "expected_delivery",
            "delivered_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Serialize an order with nested items and shipment."""

    items = OrderItemSerializer(many=True, read_only=True)
    shipment = ShipmentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_amount",
            "address",
            "phone_number",
            "payment_method",
            "status",
            "created_at",
            "updated_at",
            "items",
            "shipment",
        ]
        read_only_fields = [
            "id",
            "user",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
            "items",
            "shipment",
        ]


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating a new order from a cart."""

    cart_id = serializers.IntegerField()
    address = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    payment_method = serializers.CharField(max_length=30, default="mpesa")

    def validate_cart_id(self, value: int) -> int:
        """Ensure the cart exists, belongs to the user and is not checked out."""
        request = self.context["request"]
        try:
            cart = Cart.objects.get(pk=value, user=request.user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found.")
        if cart.checked_out:
            raise serializers.ValidationError("Cart has already been checked out.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        cart = Cart.objects.select_for_update().get(pk=validated_data["cart_id"], user=request.user)
        total = Decimal("0")
        order = Order.objects.create(
            user=request.user,
            total_amount=Decimal("0"),
            address=validated_data["address"],
            phone_number=validated_data["phone_number"],
            payment_method=validated_data["payment_method"],
            status="pending",
        )
        items = []
        for item in cart.items.select_related("product", "variation").all():
            unit_price = item.price
            line_total = unit_price * item.quantity
            total += line_total
            items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    variation=item.variation,
                    quantity=item.quantity,
                    price=unit_price,
                )
            )
            if item.variation:
                item.variation.quantity = max(item.variation.quantity - item.quantity, 0)
                item.variation.in_stock = item.variation.quantity > 0
                item.variation.save(update_fields=["quantity", "in_stock"])
            else:
                item.product.quantity = max(item.product.quantity - item.quantity, 0)
                item.product.in_stock = item.product.quantity > 0
                item.product.save(update_fields=["quantity", "in_stock"])
        OrderItem.objects.bulk_create(items)
        order.total_amount = total
        order.save(update_fields=["total_amount"])
        cart.checked_out = True
        cart.save(update_fields=["checked_out"])
        return order