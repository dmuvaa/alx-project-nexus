"""Database models for the orders app.

This module defines models representing shopping carts, orders and
shipments. Orders are created when a user checks out their cart. Each
order contains one or more ``OrderItem`` instances that capture the
quantity, price and variation of the purchased products. Shipments
record delivery information and tracking details for orders.
"""

from django.conf import settings
from django.db import models

from catalog.models import Product, ProductVariation


class Cart(models.Model):
    """A shopping cart belonging to a user.

    Each user may have multiple carts over time. A cart becomes
    immutable once it is checked out and transformed into an order.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(
        default=False,
        help_text="Indicates whether the cart has been converted to an order",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Cart #{self.id} for {self.user.username}"


class CartItem(models.Model):
    """An item in a shopping cart."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="cart_items",
    )
    variation = models.ForeignKey(
        ProductVariation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Snapshot of the price at the time of adding to cart",
    )

    class Meta:
        unique_together = ("cart", "product", "variation")

    def __str__(self) -> str:
        return f"{self.quantity} × {self.product.name}" if not self.variation else f"{self.quantity} × {self.product.name} ({self.variation.name}={self.variation.value})"


class Order(models.Model):
    """A placed order containing one or more items."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    payment_method = models.CharField(
        max_length=30,
        default="mpesa",
        help_text="Payment method selected by the user",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    """An item within an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    variation = models.ForeignKey(
        ProductVariation,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Snapshot of the unit price at the time of ordering",
    )

    class Meta:
        ordering = ["order_id"]

    def __str__(self) -> str:
        return f"{self.quantity} × {self.product.name} in Order #{self.order_id}"


class Shipment(models.Model):
    """Contains shipping details and tracking information for an order."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipment",
    )
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    carrier = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    shipped_at = models.DateTimeField(null=True, blank=True)
    expected_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["order_id"]

    def __str__(self) -> str:
        return f"Shipment for Order #{self.order_id}"