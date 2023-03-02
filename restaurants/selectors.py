from rest_framework import exceptions as rest_exceptions

from restaurants.models import Restaurant


def get_restaurant_info(id: int) -> Restaurant:
    try:
        obj = Restaurant.objects.get(id=id)
        if obj.is_active == False:
            raise rest_exceptions.ValidationError("Restaurant is not active")
    except Restaurant.DoesNotExist:
        raise rest_exceptions.ValidationError("Restaurant does not exist")

    else:
        return obj


def get_all_restaurants() -> Restaurant:
    objs = Restaurant.objects.filter(is_active=True)
    return objs
