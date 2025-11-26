"""Generic periodic tasks for housekeeping and maintenance.

Periodic tasks defined in this module are scheduled by Celery Beat and
perform background maintenance functions. They operate across apps and
should be idempotent and safe to run multiple times.
"""

from celery import shared_task
from django.utils import timezone

from catalog.models import Product


@shared_task
def disable_out_of_stock_products() -> None:
    """Mark products as out of stock when their quantity is zero.

    This task scans the catalog for products where ``quantity`` is zero
    but ``in_stock`` is still set to True. It then updates the
    ``in_stock`` flag accordingly. Periodic execution ensures product
    availability statuses remain accurate over time.
    """
    updated = Product.objects.filter(quantity=0, in_stock=True).update(in_stock=False)
    print(f"Disabled {updated} products that were out of stock at {timezone.now()}")