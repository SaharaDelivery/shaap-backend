from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions
from restaurants.models import MenuItem, Order, OrderAddress, OrderItem, Restaurant

from users.models import CustomUser
from utils.generators import generate_default_username


@transaction.atomic
def create_user(data: dict) -> CustomUser:
    """This function creates a user.

    Args:
        data (dict): The user's email and password

    Raises:
        rest_exceptions.ValidationError: If the user's data is invalid

    Returns:
        CustomUser: The created user
    """
    try:
        default_username = generate_default_username(email=data["email"])
        user = CustomUser(email=data["email"], username=default_username)
        user.set_password(data["password"])
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return user


@transaction.atomic
def setup_user_account(user_id: int, data: dict) -> CustomUser:
    """This function sets up a user's account.

    Args:
        user_id (int): The user's id
        data (dict): The user's first name, last name and phone number

    Raises:
        rest_exceptions.NotFound: When the user with the user_id does not exist
        rest_exceptions.ValidationError: When the user's data is invalid

    Returns:
        CustomUser: The user's account
    """
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        raise rest_exceptions.NotFound()

    try:
        for key, value in data.items():
            setattr(user, key, value)
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return user


@transaction.atomic
def edit_user_account(user: CustomUser, data: dict) -> CustomUser:
    """This function edits a user's account details (first name, last name and phone number).

    Args:
        user (CustomUser): The user
        data (dict): the data to be updated
    Raises:
        rest_exceptions.ValidationError: When the user's data is invalid

    Returns:
        CustomUser: The updated user account
    """
    try:
        for key, value in data.items():
            setattr(user, key, value)
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return user


@transaction.atomic
def login_user(user: CustomUser) -> None:
    try:
        user.last_login = timezone.now()
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return user


@transaction.atomic
def place_order(
    user: CustomUser, restaurant: Restaurant, menu_item: MenuItem, quantity: int
) -> Order:
    """This function places an order

    Args:
        user (CustomUser): The user object
        restaurant (Restaurant): The restaurant object
        menu_item (MenuItem): The menu item object
        quantity (int): The quantity of the menu item

    Raises:
        rest_exceptions.ValidationError: When the order or order item is invalid

    Returns:
        Order: The created order object
    """
    if Order.objects.filter(user=user, restaurant=restaurant, paid=False).exists():
        try:
            order_item = OrderItem(order=order, menu_item=menu_item)
            order_item.full_clean()
            order_item.save()
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(e)

        else:
            return order

    else:
        try:
            order = Order(user=user, restaurant=restaurant)
            order.full_clean()
            order.save()
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(e)

        try:
            order_item = OrderItem(order=order, menu_item=menu_item)
            order_item.full_clean()
            order_item.save()
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(e)

        else:
            return order


@transaction.atomic
def add_order_address(user: CustomUser, data: dict) -> OrderAddress:
    """This function adds the address to an order

    Args:
        user (CustomUser): The user object
        order_id (str): The order id
        data (dict): The address data

    Returns:
        OrderAddress: The created order address object
    """
    try:
        obj = OrderAddress(user=user, **data)
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return obj


@transaction.atomic
def edit_order_address(user: CustomUser, data: dict, address_id: int):
    """This function edits the address of an order

    Args:
        user (CustomUser): The user object
        data (dict): The address data
        address_id (int): The address id

    Raises:
        rest_exceptions.NotFound: If address does not exist
    """
    try:
        obj = OrderAddress.objects.get(user=user, id=address_id)
    except OrderAddress.DoesNotExist:
        raise rest_exceptions.NotFound("Address does not exist")

    try:
        for key, value in data.items():
            setattr(obj, key, value)
        obj.full_clean()
        obj.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return obj


@transaction.atomic
def add_order_item(order: Order, menu_item: MenuItem, quantity: int) -> OrderItem:
    """This function adds a menu item to an order

    Args:
        order (Order): The order object
        menu_item (MenuItem): The menu item object
        quantity (int): The quantity of the menu item

    Returns:
        OrderItem: The created order item object
    """

    if OrderItem.objects.filter(order=order, menu_item=menu_item).exists():
        try:
            obj = OrderItem.objects.get(order=order, menu_item=menu_item)
            obj.quantity += quantity
            obj.full_clean()
            obj.save()
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(e)

    else:
        try:
            obj = OrderItem(order=order, menu_item=menu_item, quantity=quantity)
            obj.full_clean()
            obj.save()
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(e)

    return obj


@transaction.atomic
def reduce_order_item_quantity(order_item_id: int) -> None:
    """This function removes a menu item from an order

    Args:
        order_item_id (int): The order item id

    Returns:
        None: If the order item is deleted
        OrderItem: if the order item quantity is reduced
    """
    obj = get_object_or_404(OrderItem, id=order_item_id)
    if obj.quantity > 1:
        try:
            obj.quantity -= 1
            obj.full_clean()
            obj.save()
            return obj
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(e)
    else:
        obj.delete()
        return None


@transaction.atomic
def delete_order_item(order_item_id: int) -> None:
    """This function deletes an order item

    Args:
        order_item_id (int): The order item id

    Returns:
        None: If the order item is deleted
    """
    try:
        obj = OrderItem.objects.get(id=order_item_id)
    except OrderItem.DoesNotExist:
        raise rest_exceptions.NotFound("Order item does not exist")

    else:
        obj.delete()
        return None
