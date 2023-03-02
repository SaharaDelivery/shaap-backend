from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import BasePermission

from restaurants.models import RestaurantStaff


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.is_admin)
        except AttributeError as e:
            raise rest_exceptions.PermissionDenied(e)


class IsRestaurantAdmin(BasePermission):
    """
    Allows access only to restaurant admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise rest_exceptions.NotAuthenticated("User is not authenticated")
        obj = RestaurantStaff.objects.get(user=request.user)
        try:
            return bool(request.user and obj.is_restaurant_admin)
        except AttributeError as e:
            raise rest_exceptions.PermissionDenied(e)
