"""Asynchronous tasks related to user operations."""

from celery import shared_task
from django.contrib.auth.models import User


@shared_task
def send_welcome_email(user_id: int) -> None:
    """Send a welcome email to a newly registered user.

    This task is executed asynchronously via Celery. In a real
    implementation, the body of this function would integrate with an
    external email service provider such as SendGrid, Amazon SES, or
    Django’s own email backend. Here it simply prints a log message.

    Args:
        user_id: The primary key of the user to send the welcome message to.
    """
    try:
        user = User.objects.get(pk=user_id)
        # In a real implementation, you would send an actual email here.
        print(f"Sending welcome email to {user.email} ({user.username})")
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist")