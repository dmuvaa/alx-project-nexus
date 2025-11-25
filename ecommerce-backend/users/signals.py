"""Signal handlers for user events."""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile
from .tasks import send_welcome_email


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User, created: bool, **kwargs) -> None:
    """Create or update the user profile when a ``User`` instance is saved.

    On creation, a new ``UserProfile`` is created and a welcome email is sent
    asynchronously via Celery. On update, the existing profile is saved to
    propagate any changes to related fields.

    Args:
        sender: The model class ``User``.
        instance: The actual instance being saved.
        created: Boolean; True if the instance is newly created.
        **kwargs: Additional keyword arguments provided by the signal.
    """
    if created:
        UserProfile.objects.create(user=instance)
        send_welcome_email.delay(instance.pk)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()