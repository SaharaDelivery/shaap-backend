from rest_framework import exceptions as rest_exceptions

from restaurants.models import Menu, MenuItem, Restaurant


def get_restaurant_info(id: int) -> Restaurant:
    """This function gets a restaurant object by id

    Args:
        id (int): The id of the restaurant

    Raises:
        rest_exceptions.NotFound: If restaurant does not exist

    Returns:
        Restaurant: The restaurant object
    """
    try:
        obj = Restaurant.objects.filter(id=id, is_active=True)
    except Restaurant.DoesNotExist:
        raise rest_exceptions.NotFound("Restaurant does not exist")

    else:
        return obj


def get_all_restaurants() -> Restaurant:
    """This function gets all active restaurants

    Returns:
        Restaurant: The restaurant objects
    """
    objs = Restaurant.objects.filter(is_active=True)
    return objs


def get_restaurant_menu(id: int) -> Menu:
    """This function gets a menu object by id

    Args:
        id (int): The id of the menu

    Raises:
        rest_exceptions.NotFound: If menu does not exist

    Returns:
        Menu: The menu object
    """
    try:
        obj = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        raise rest_exceptions.NotFound("Menu does not exist")

    else:
        return obj


def get_all_restaurant_menus(restaurant_id: int) -> Menu:
    """This function gets all active menus of a restaurant

    Args:
        restaurant_id (int): The id of the restaurant

    Raises:
        rest_exceptions.NotFound: If restaurant does not exist

    Returns:
        Menu: The Menu Objects
    """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        raise rest_exceptions.NotFound("Restaurant does not exist")

    else:
        objs = Menu.objects.filter(restaurant=restaurant, is_active=True)
    return objs


def get_archived_restaurant_menus(restaurant_id: int) -> Menu:
    """This function gets all archived menus of a restaurant

    Args:
        restaurant_id (int): The id of the restaurant

    Raises:
        rest_exceptions.NotFound: If restaurant does not exist

    Returns:
        Menu: The Archived Menu Objects
    """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        objs = Menu.objects.filter(restaurant=restaurant, is_active=False)
    except (Restaurant.DoesNotExist, Menu.DoesNotExist) as e:
        raise rest_exceptions.NotFound(e)

    else:
        return objs


def get_restaurant_menu_item(id: int) -> MenuItem:
    """This function gets a menu item object by id

    Args:
        id (int): The id of the menu item

    Raises:
        rest_exceptions.NotFound: If menu item does not exist

    Returns:
        MenuItem: The menu item object
    """
    try:
        obj = MenuItem.objects.get(id=id)
    except MenuItem.DoesNotExist:
        raise rest_exceptions.NotFound("Menu Item does not exist")

    else:
        return obj


def get_all_restaurant_menu_items(id: int) -> MenuItem:
    """This function gets all active menu items of a menu

    Args:
        menu_id (int): The id of the menu

    Raises:
        rest_exceptions.NotFound: If menu does not exist

    Returns:
        MenuItem: The Menu Item Objects
    """
    try:
        menu = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        raise rest_exceptions.NotFound("Menu does not exist")

    else:
        objs = MenuItem.objects.filter(menu=menu, is_active=True)
    return objs
