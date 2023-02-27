from django.db import transaction
from django.utils import timezone
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions

from users.models import CustomUser


@transaction.atomic
def create_user(data: dict) -> CustomUser:
    try:
        user = CustomUser(**data)
        user.set_password(data["password"])
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return user


@transaction.atomic
def edit_user_account(user: CustomUser, data: dict) -> CustomUser:
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
def disable_user_account(user: CustomUser) -> None:
    try:
        user.is_active = False
        user.full_clean()
        user.save()
    except django_exceptions.ValidationError as e:
        raise rest_exceptions.ValidationError(e)

    else:
        return user
