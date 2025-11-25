"""Serializers for user registration and profile management.

Serializers convert complex types such as Django models into native
Python datatypes that can then be rendered into JSON, XML or other
content types. They also provide deserialization, allowing parsed
data to be converted back into complex types after first validating
the incoming data.
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the ``UserProfile`` model."""

    class Meta:
        model = UserProfile
        fields = ["phone", "address"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user.

    Accepts nested data for the associated ``UserProfile`` and writes
    both objects atomically. Validates the password using Django’s
    built‑in password validators.
    """

    password = serializers.CharField(write_only=True, required=True)
    profile = UserProfileSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile"]

    def validate_password(self, value: str) -> str:
        """Validate the provided password using Django’s validators."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Create a user and an associated profile if provided."""
        profile_data = validated_data.pop("profile", {}) or {}
        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )
        # Create or update the profile
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user information."""

    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["username", "email"]

    def update(self, instance: User, validated_data):
        """Update the user and their profile in a nested way."""
        profile_data = validated_data.pop("profile", {})
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        if profile_data:
            UserProfile.objects.update_or_create(user=instance, defaults=profile_data)
        return instance