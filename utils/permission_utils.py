from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.is_admin)
        except AttributeError as e:
            raise rest_exceptions.PermissionDenied(e)
