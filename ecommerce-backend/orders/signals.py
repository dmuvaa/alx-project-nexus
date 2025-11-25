"""Signal handlers for order events."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, Shipment
from .tasks import send_order_confirmation


@receiver(post_save, sender=Order)
def create_shipment_and_notify(sender, instance: Order, created: bool, **kwargs) -> None:
    """Create a shipment record and send confirmation when a new order is placed."""
    if created:
        Shipment.objects.create(order=instance)
        send_order_confirmation.delay(instance.pk)