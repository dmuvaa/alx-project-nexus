"""API views for user registration and profile management."""

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Create a new user along with an optional profile."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete the authenticated user's profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the currently authenticated user."""
        return self.request.user
    
class UserListView(generics.ListAPIView):
    """List all users (admin-only)."""

    queryset = get_user_model().objects.all().select_related("userprofile")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
