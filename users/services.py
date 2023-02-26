from django.db import transaction
from django.utils import timezone
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions

from users.models import CustomUser


@transaction.atomic
def create_user(data: dict) -> CustomUser:
    user = CustomUser(**data)
    user.set_password(data["password"])
    user.full_clean()
    user.save()


@transaction.atomic
def edit_user_profile(user: CustomUser, data: dict) -> None:
    try:
        for key, value in data.items():
            setattr(user, key, value)
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)


def login_user(user: CustomUser) -> None:
    user.last_login = timezone.now()
    user.full_clean()
    user.save()
