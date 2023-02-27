from django.db import models

from users.models import CustomUser


class Restaurant(models.Model):
    # logo = models.ImageField(upload_to="restaurants/logo/", null=True, blank=True)
    # cover_photo = models.ImageField(upload_to="restaurants/cover_photo/", null=True, blank=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return f"{self.name} | {self.restaurant.name}"


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_items")
    # image = models.ImageField(upload_to="restaurants/menu_items/", null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.name} | {str(self.price)} | {self.menu.name} | {self.menu.restaurant.name}"
