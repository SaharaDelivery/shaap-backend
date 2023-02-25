from django.db import transaction
from django.utils import timezone

from users.models import CustomUser


@transaction.atomic
def create_user(data: dict) -> CustomUser:
    user = CustomUser(**data)
    user.set_password(data["password"])
    user.full_clean()
    user.save()


def login_user(user: CustomUser) -> None:
    user.last_login = timezone.now()
    user.full_clean()
    user.save()
