"""API views for handling payments."""

from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from .tasks import process_mpesa_payment


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Allow users to view their own payment records."""

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return payments belonging to the current user or all if admin."""
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)


class CreatePaymentView(generics.CreateAPIView):
    """Initiate a new payment and trigger an MPesa STK push.

    The endpoint accepts the phone number, amount and description of the
    payment, plus an optional ``order_id``. It creates a ``Payment``
    record associated with the authenticated user and dispatches a
    Celery task to call the MPesa API asynchronously.
    """

    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Save the payment and dispatch the Celery task."""
        payment = serializer.save()
        # Dispatch asynchronous task to initiate payment
        process_mpesa_payment.delay(payment.pk)

    def create(self, request, *args, **kwargs):  # noqa: D401
        """Override to return the payment details after creation."""
        response = super().create(request, *args, **kwargs)
        # Provide additional feedback in the response
        return Response(
            {
                "message": "Payment initiated. Await STK prompt on your phone.",
                "payment": response.data,
            },
            status=status.HTTP_201_CREATED,
        )