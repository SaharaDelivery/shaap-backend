import random
from users.models import CustomUser


def generate_default_username(email: str) -> str:
    """This function generates a default username for a new user.

    Args:
        email (str): The user's email

    Returns:
        str: The default username
    """
    default_username = email.split("@")[0]

    try:
        print("a")
        obj = CustomUser.objects.get(username=default_username)
    except CustomUser.DoesNotExist:
        pass

    else:
        default_username = (
            f"{default_username}{CustomUser.objects.count()}{random.randint(0, 100)}"
        )

    return default_username
