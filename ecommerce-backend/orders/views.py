"""API views for carts, orders and shipments."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Cart, CartItem, Order, Shipment
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    ShipmentSerializer,
)


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    """View or list the authenticated user's carts.

    A user may have multiple carts over time. By default this viewset
    lists all carts belonging to the user. Individual carts can be
    retrieved by ID if they belong to the user.
    """

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """Create, update and delete items in the user's active cart."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return items belonging to the user's current open cart. If none
        exists, return an empty queryset. Users cannot manipulate items
        once the cart has been checked out."""
        cart = Cart.objects.filter(user=self.request.user, checked_out=False).first()
        return cart.items.all() if cart else CartItem.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return AddCartItemSerializer
        if self.action in {"update", "partial_update"}:
            return UpdateCartItemSerializer
        return CartItemSerializer

    def perform_create(self, serializer):
        """Ensure there is an active cart. Create one if not present."""
        cart, _ = Cart.objects.get_or_create(user=self.request.user, checked_out=False)
        serializer.save(cart=cart)

    def perform_destroy(self, instance):
        instance.delete()


class OrderViewSet(viewsets.ModelViewSet):
    """Create and list orders for the authenticated user."""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save()


class ShipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Read‑only viewset for shipment tracking.

    Users can view the status of their own shipments. Administrators
    may view all shipments.
    """

    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Shipment.objects.select_related("order", "order__user").all()
        return Shipment.objects.select_related("order", "order__user").filter(order__user=user)