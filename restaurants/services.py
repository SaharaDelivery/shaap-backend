from django.db import transaction
from django.utils import timezone
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions

from restaurants.models import Cuisine, Menu, MenuItem, Restaurant, RestaurantStaff
from restaurants.selectors import get_restaurant_menu
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


@transaction.atomic
def create_menu(data: dict, creator: CustomUser) -> Menu:
    """This function creates a menu

    Args:
        data (dict): a dictionary containing the details of the menu
        creator (CustomUser): The creator of the menu

    Returns:
        Menu: The created menu obj
    """
    try:
        restaurant = Restaurant.objects.get(id=data.pop("restaurant"))
        cuisine = Cuisine.objects.get(id=data.pop("cuisine"))
        obj = Menu(restaurant=restaurant, cuisine=cuisine, **data)
        obj.creator = creator
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return obj


@transaction.atomic
def update_restaurant_menu(id: int, data: dict) -> Menu:
    """This function updates the restaurant menu

    Args:
        id (int): The ID of the menu
        data (dict): The details of the menu that you want to update

    Returns:
        Menu: The updated menu obj
    """
    menu = Menu.objects.get(id=id)
    try:
        for key, value in data.items():
            if key == "cuisine":
                value = Cuisine.objects.get(id=value)
            setattr(menu, key, value)
        menu.full_clean()
        menu.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)


@transaction.atomic
def archive_menu(id: int) -> Menu:
    """This function archives a menu

    Args:
        id (int): The id of the menu

    Returns:
        Menu: The archived menu obj
    """
    try:
        obj = Menu.objects.get(id=id)
    except Menu.DoesNotExist as e:
        raise rest_exceptions.NotFound(e)

    try:
        obj.is_active = False
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    return obj


@transaction.atomic
def delete_menu(id: int) -> None:
    """This function deletes a menu

    Args:
        id (int): The id of the menu

    Returns:
        None
    """
    try:
        obj = Menu.objects.get(id=id)
    except Menu.DoesNotExist as e:
        raise rest_exceptions.NotFound(e)

    else:
        obj.delete()

    return None


@transaction.atomic
def create_menu_item(data: dict, creator: CustomUser) -> MenuItem:
    """This function creates a menu item

    Args:
        data (dict): The details of the menu item
        creator (CustomUser): The creator of the menu item

    Returns:
        MenuItem: The created menu item obj
    """
    menu = get_restaurant_menu(id=data.pop("menu"))
    try:
        obj = MenuItem(menu=menu, **data)
        obj.creator = creator
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return obj


@transaction.atomic
def update_restaurant_menu_item(id: int, data: dict) -> MenuItem:
    """This function updates a menu item

    Args:
        id (int): The ID of the menu item
        data (dict): The details of the menu item that you want to update

    Returns:
        MenuItem: The updated menu item obj
    """
    try:
        obj = MenuItem.objects.get(id=id)
    except MenuItem.DoesNotExist as e:
        raise rest_exceptions.NotFound(e)

    try:
        for key, value in data.items():
            setattr(obj, key, value)
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    return obj


@transaction.atomic
def archive_menu_item(id: int) -> MenuItem:
    """This function archives a menu item

    Args:
        id (int): The ID of the menu item

    Returns:
        MenuItem: The archived menu item obj
    """
    try:
        obj = MenuItem.objects.get(id=id)
    except MenuItem.DoesNotExist as e:
        raise rest_exceptions.NotFound(e)

    try:
        obj.is_active = False
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    return obj


@transaction.atomic
def delete_menu_item(id: int) -> None:
    """This function deletes a menu item

    Args:
        id (int): The ID of the menu item

    Returns:
        None
    """
    try:
        obj = MenuItem.objects.get(id=id)
    except MenuItem.DoesNotExist as e:
        raise rest_exceptions.NotFound(e)

    else:
        obj.delete()

    return None
