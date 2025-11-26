"""Models for payment processing and records."""

from django.conf import settings
from django.db import models


class Payment(models.Model):
    """Record of a payment transaction.

    Payments may be associated with a specific order or represent
    standalone top‑ups. The status field tracks the progress of the
    transaction (pending, success, failed) and the ``method`` field
    records the payment mechanism used. For MPesa payments the
    transaction ID corresponds to the ``CheckoutRequestID`` returned
    from Safaricom's API. Other payment gateways can supply their own
    identifiers.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    order = models.ForeignKey(
        "orders.Order",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="payments",
        help_text="Optional order this payment is settling",
    )
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    method = models.CharField(
        max_length=30,
        default="mpesa",
        help_text="Payment method used (e.g. mpesa, card)",
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return a human‑readable representation of the payment record."""
        return f"Payment #{self.id} by {self.user.username}" if self.user_id else f"Payment #{self.id}"