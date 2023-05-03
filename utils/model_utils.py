from django.db.models import Model

from rest_framework import exceptions as rest_exceptions


def get_object_or_rest_404(obj: Model, **kwargs) -> Model:
    """This is a custom function that returns an object or raises a REST 404 exception.

    Args:
        obj (Model): The model object.

    Returns:
        Model: The model object.
    """
    try:
        return obj.objects.get(**kwargs)
    except (obj.DoesNotExist, Exception) as e:
        raise rest_exceptions.NotFound(e)
