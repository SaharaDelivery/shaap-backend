from django.db import transaction
from django.utils import timezone
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions

from restaurants.models import Restaurant, RestaurantStaff
from users.models import CustomUser


@transaction.atomic
def register_restaurant(data: dict, creator: CustomUser) -> Restaurant:
    """This function registers a restaurant

    Args:
        data (dict): The details of the restaurant

    Returns:
        Restaurant: The created restaurant obj
    """
    try:
        restaurant = Restaurant(**data)
        restaurant.creator = creator
        restaurant.full_clean()
        restaurant.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)


@transaction.atomic
def update_restaurant_info(id: int, data: dict):
    """This function updates the restaurant info

    Args:
        id (int): The ID of the restaurant
        data (dict): a dictionary containing fields you want to update
    """
    try:
        restaurant = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        raise rest_exceptions.NotFound("Restaurant not found")

    try:
        for key, value in data.items():
            setattr(restaurant, key, value)
        restaurant.full_clean()
        restaurant.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    return restaurant


@transaction.atomic
def disable_restaurant(id: int) -> Restaurant:
    """This function disables a restaurant

    Args:
        id (int): The ID of the restaurant

    Returns:
        Restaurant: The disabled restaurant obj
    """
    try:
        restaurant = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        raise rest_exceptions.NotFound("Restaurant not found")

    restaurant.is_active = False
    restaurant.full_clean()
    restaurant.save()
    return restaurant


@transaction.atomic
def login_restaurant_staff(user: CustomUser) -> CustomUser:
    """This function logs in a restaurant staff

    Args:
        user (CustomUser): The restaurant staff

    Returns:
        CustomUser: The restaurant staff with the last_login updated
    """
    try:
        obj = RestaurantStaff.objects.get(user=user)
    except RestaurantStaff.DoesNotExist:
        raise rest_exceptions.PermissionDenied()

    try:
        obj.last_login = timezone.now()
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)
