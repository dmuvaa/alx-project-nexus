"""Application configuration for the orders app."""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Configuration for the orders app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self) -> None:
        """Import signal handlers when the app is ready."""
        import orders.signals