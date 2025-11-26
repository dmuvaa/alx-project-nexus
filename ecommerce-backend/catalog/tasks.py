"""Asynchronous tasks related to catalog operations.

These tasks run in the background via Celery to perform potentially
time‑consuming operations such as updating stock levels. Running such
tasks asynchronously avoids blocking HTTP request threads and improves
the responsiveness of the API.
"""

from celery import shared_task

from .models import Product, ProductVariation


@shared_task
def update_product_stock(product_id: int, quantity: int) -> None:
    """Update the stock quantity for a given product.

    Args:
        product_id: The primary key of the product to update.
        quantity: The new quantity to set.
    """
    try:
        product = Product.objects.get(pk=product_id)
        product.quantity = quantity
        product.in_stock = quantity > 0
        product.save(update_fields=["quantity", "in_stock"])
        print(f"Updated stock for {product.name} to {quantity}")
    except Product.DoesNotExist:
        print(f"Product with id {product_id} does not exist")


@shared_task
def update_variation_stock(variation_id: int, quantity: int) -> None:
    """Update the stock quantity for a given product variation.

    When a variation's quantity changes, the parent product's ``in_stock``
    flag may need to be updated accordingly. If all variations and the
    product quantity are zero, the product is marked out of stock.

    Args:
        variation_id: The primary key of the variation to update.
        quantity: The new quantity to set on the variation.
    """
    try:
        variation = ProductVariation.objects.select_related("product").get(pk=variation_id)
        variation.quantity = quantity
        variation.in_stock = quantity > 0
        variation.save(update_fields=["quantity", "in_stock"])
        # Determine if the parent product should still be considered in stock
        product = variation.product
        has_stock = product.quantity > 0 or product.variations.filter(in_stock=True).exists()
        if product.in_stock != has_stock:
            product.in_stock = has_stock
            product.save(update_fields=["in_stock"])
        print(f"Updated stock for variation {variation} to {quantity}")
    except ProductVariation.DoesNotExist:
        print(f"Variation with id {variation_id} does not exist")