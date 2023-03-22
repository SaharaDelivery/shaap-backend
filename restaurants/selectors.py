from rest_framework import exceptions as rest_exceptions
from common.choices import ORDER_STATUS

from restaurants.models import (
    Cuisine,
    Menu,
    MenuItem,
    Order,
    OrderAddress,
    OrderItem,
    Restaurant,
)
from users.models import CustomUser


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


def get_all_restaurants_with_cuisine(cuisine: str) -> Restaurant:
    """This function gets all active restaurants with a specific cuisine

    Args:
        cuisine (str): The cuisine of the restaurant

    Returns:
        Restaurant: The list of restaurants that match the cuisine
    """
    try:
        cuisine = Cuisine.objects.get(name=cuisine)
    except Cuisine.DoesNotExist:
        raise rest_exceptions.NotFound("Cuisine does not exist")

    else:
        objs = Restaurant.objects.filter(cuisine__in=[cuisine], is_active=True)
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


def get_all_orders_based_on_status(user: CustomUser, status: str) -> Order:
    """This function gets all orders of a user based on the status

    Args:
        user (CustomUser): The user object

    Returns:
        Order: The Order Objects
    """
    valid_status = [s[0] for s in ORDER_STATUS]
    if status in valid_status:
        objs = Order.objects.filter(user=user, status=status)
    else:
        raise rest_exceptions.ValidationError("Invalid status")
    return objs


def get_user_order_history(user: CustomUser) -> Order:
    """This functiom gets the order history of a user

    Args:
        user (CustomUser): The user object

    Returns:
        Order: The Order History sorted on date_created
    """
    orders = Order.objects.filter(user=user, paid=True, status="delivered").order_by(
        "-date_created"
    )
    return orders


def get_all_order_items(order_id: int) -> OrderItem:
    """This function gets all order items of an order

    Args:
        id (int): The id of the order

    Raises:
        rest_exceptions.NotFound: If order does not exist

    Returns:
        OrderItem: The Order Item Objects
    """
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        raise rest_exceptions.NotFound("Order does not exist")

    else:
        objs = OrderItem.objects.filter(order=order)
        return objs


def get_saved_user_addresses(user: CustomUser) -> OrderAddress:
    """This function gets the saved addresses of a user

    Args:
        user (CustomUser): The user object

    Returns:
        OrderAddress: The saved addresses of a user
    """
    objs = OrderAddress.objects.filter(user=user, saved=True)
    return objs
