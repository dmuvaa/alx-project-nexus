"""Asynchronous tasks related to orders and shipments."""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Order


@shared_task
def send_order_confirmation(order_id: int) -> None:
    """Send an email confirming that an order has been placed.

    This task demonstrates how one might send an order confirmation
    asynchronously. In practice, integrate with a real email backend.

    Args:
        order_id: The primary key of the order to confirm.
    """
    try:
        order = Order.objects.select_related("user").get(pk=order_id)
        subject = f"Order #{order.id} Confirmation"
        message = (
            f"Dear {order.user.username},\n\n"
            f"Thank you for your purchase! Your order #{order.id} has been received "
            f"and is currently {order.status}. We will notify you when it ships.\n\n"
            f"Total: {order.total_amount}\n"
            f"Shipping to: {order.address}\n\n"
            "Regards,\n"
            "E‑Commerce Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or "no-reply@example.com",
            [order.user.email],
            fail_silently=True,
        )
        print(f"Sent order confirmation email for Order #{order.id}")
    except Order.DoesNotExist:
        print(f"Order {order_id} does not exist, cannot send confirmation")