from datetime import datetime
from django.db.models import Q

from restaurants.models import Restaurant


def filter_restaurants(params: dict) -> Restaurant:
    """This function filters restaurants based on the below parameters
    Params:
        name (str): The name of the restaurant
        cuisine (list(id)): The cuisine(s) of the restaurant
        is_opened (bool): If the restaurant is opened or not
        rating (int): The rating of the restaurant
    Args:
        params (dict): The parameters to filter the restaurants

    Returns:
        Restaurant: The restaurants that fit the criteria
    """
    current_time = datetime.now().time()
    queryset = Restaurant.objects.all()
    name = params.get("name", None)
    cuisine = params.get("cuisine", None)
    is_open = params.get("is_opened", None)
    rating = params.get("rating", None)
    if name is not None:
        queryset = queryset.filter(name__icontains=name)
    if cuisine is not None:
        if len(cuisine) == 1:
            queryset = queryset.filter(cuisine__in=[cuisine])
        else:
            queryset = queryset.filter(cuisine__in=cuisine.split(","))
    if is_open is not None:
        queryset = Restaurant.objects.filter(
            Q(opening_time__lte=current_time) & Q(closing_time__gte=current_time)
        )
    if rating is not None:
        queryset = queryset.filter(rating__gte=rating)

    return queryset
