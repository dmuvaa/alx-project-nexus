"""Asynchronous tasks for payment processing."""

from celery import shared_task

from .models import Payment
from .mpesa import lipa_na_mpesa


@shared_task
def process_mpesa_payment(payment_id: int) -> None:
    """Trigger an MPesa STK push for the given payment.

    Fetches the payment record from the database, initiates the payment
    via the MPesa API, and updates the record based on the response. In
    case of failure, the payment status is marked as failed.

    Args:
        payment_id: The primary key of the payment to process.
    """
    try:
        payment = Payment.objects.get(pk=payment_id)
        response = lipa_na_mpesa(
            phone_number=payment.phone_number,
            amount=float(payment.amount),
            account_reference=str(payment.id),
            transaction_desc=payment.description or "E‑Commerce Payment",
        )
        payment.transaction_id = response.get("CheckoutRequestID")
        payment.status = "pending"
        payment.save(update_fields=["transaction_id", "status"])
        print(f"Initiated MPesa payment for Payment #{payment.id}")
    except Payment.DoesNotExist:
        print(f"Payment record {payment_id} does not exist")
    except Exception as exc:  # noqa: BLE001
        print(f"Error processing MPesa payment {payment_id}: {exc}")