from restaurants.models import Order
from users.models import CustomUser


def get_all_orders(user: CustomUser) -> Order:
    """This function returns all paid orders belonging to a user 

    Args:
        user (CustomUser): The user

    Returns:
        Order: All the orders he paid for
    """
    return Order.objects.filter(user=user, paid=True)