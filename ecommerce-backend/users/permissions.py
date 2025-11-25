"""Custom permission classes for the users app."""

from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """Allow users to retrieve/update their own profile or admin users to access any profile."""

    def has_object_permission(self, request, view, obj) -> bool:
        return bool(request.user and (obj == request.user or request.user.is_staff))