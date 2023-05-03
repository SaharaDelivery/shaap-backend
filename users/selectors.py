from typing import Tuple, Optional

from users.models import CustomUser
from restaurants.models import Order
from utils.model_utils import get_object_or_rest_404


def get_existing_user_restaurant_order(
    user: CustomUser, restaurant_id: int
) -> Tuple[Optional[Order], bool]:
    """This function checks if the user has an existing order for the restaurant.

    Args:
        user (CustomUser): The user object.
        restaurant_id (int): The restaurant id.

    Returns:
        Tuple[Optional[Order], bool]: (Order, True) if order exists, else (None, False).
    """
    try:
        order = Order.objects.get(restaurant__id=restaurant_id, paid=False, user=user)
    except Order.DoesNotExist:
        return None, False

    return order, True


def get_user_order(user: CustomUser, order_id: str) -> Order:
    """This function returns the order object

    Args:
        user (CustomUser): The user object.
        order_id (str): The order id.

    Returns:
        Order: The user's order object.

    Raises:
        Order.DoesNotExist: If the order does not exist.
    """
    return get_object_or_rest_404(Order, order_id=order_id, user=user)
