"""URL routes for the payments app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, CreatePaymentView


router = DefaultRouter()
router.register(r"records", PaymentViewSet, basename="payment")


urlpatterns = [
    path("", include(router.urls)),
    path("initiate/", CreatePaymentView.as_view(), name="payment-initiate"),
]