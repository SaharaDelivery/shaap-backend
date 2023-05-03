from typing import Tuple, Optional

from users.models import CustomUser
from restaurants.models import Order

def get_existing_user_restaurant_order(user: CustomUser, restaurant_id: int) -> Tuple[Optional[Order], bool]:
    try:
        order = Order.objects.get(restaurant__id=restaurant_id)
    except Order.DoesNotExist:
        return None, False
    
    return order, True