from django.db import transaction

from users.models import CustomUser


@transaction.atomic
def create_user(data: dict) -> CustomUser:
    user = CustomUser(**data)
    user.full_clean()
    user.save()
