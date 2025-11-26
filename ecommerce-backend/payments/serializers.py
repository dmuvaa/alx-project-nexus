"""Serializers for payment operations."""

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serialize payment instances for listing and detail views."""

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "order",
            "phone_number",
            "amount",
            "transaction_id",
            "status",
            "method",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "transaction_id",
            "status",
            "created_at",
            "updated_at",
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new payment request."""

    # Allow associating a payment with an order by ID if provided. The view
    # will enforce that the order belongs to the requesting user and has
    # not already been paid.
    order_id = serializers.IntegerField(
        write_only=True,
        required=False,
        help_text="Optional order id this payment should settle",
    )

    class Meta:
        model = Payment
        fields = ["phone_number", "amount", "description", "order_id"]

    def validate_order_id(self, value: int) -> int:
        """Ensure the referenced order exists and belongs to the user."""
        from orders.models import Order  # local import to avoid circular dependency
        request = self.context["request"]
        try:
            order = Order.objects.get(pk=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")
        if order.user != request.user:
            raise serializers.ValidationError("Cannot pay for someone else's order.")
        if order.payments.filter(status="success").exists():
            raise serializers.ValidationError("Order is already paid.")
        return value

    def create(self, validated_data):
        """Assign the payment to the current user and optionally an order."""
        user = self.context["request"].user
        order_id = validated_data.pop("order_id", None)
        payment = Payment.objects.create(user=user, **validated_data)
        if order_id:
            payment.order_id = order_id
            payment.save(update_fields=["order"])
        return payment