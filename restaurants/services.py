from django.db import transaction
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions

from restaurants.models import Restaurant
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
