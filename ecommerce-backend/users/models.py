"""Models for the users app.

Defines additional user‑related models such as ``UserProfile`` for
storing extra information not provided by Django’s default ``User``
model. Each profile is automatically created via a signal when a user
is registered.
"""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extend the built‑in Django User model with additional fields."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        """Return the username when converting the profile to string."""
        return self.user.get_username()