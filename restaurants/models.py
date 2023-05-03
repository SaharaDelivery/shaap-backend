import uuid

from django.db import models

from rest_framework import exceptions as rest_exceptions

from simple_history.models import HistoricalRecords

from users.models import CustomUser

from common.choices import ORDER_STATUS


class Restaurant(models.Model):
    cover_photo = models.ImageField(
        upload_to="restaurants/cover_sphoto/", blank=True, null=True
    )
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    cuisine = models.ManyToManyField("Cuisine", related_name="restaurants", blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name


class RestaurantStaff(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_restaurant_staff = models.BooleanField(default=True)
    is_restaurant_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.restaurant.name

    class Meta:
        verbose_name_plural = "Restaurant Staff"


class Cuisine(models.Model):
    name = models.CharField(max_length=200, unique=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, default=1)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.name} | {self.restaurant.name}"


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_items")
    image = models.ImageField(
        upload_to="restaurants/menu_items/", null=True, blank=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.name} | {str(self.price)} | {self.menu.name} | {self.menu.restaurant.name}"


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paid = models.BooleanField(default=False)
    order_address = models.ForeignKey(
        "OrderAddress", on_delete=models.CASCADE, null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderID: {self.order_id} | {self.user.email} | {self.restaurant.name} | Paid: {self.paid}" 


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order.order_id} | {self.menu_item.name} | {self.quantity}"


class OrderAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_1 = models.TextField()
    address_2 = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    saved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} | {self.saved}"

    def clean(self) -> None:
        obj = OrderAddress.objects.filter(user=self.user, saved=True)
        if len(obj) >= 2:
            raise rest_exceptions.ValidationError("You can only have 2 saved addresses")
        return super().clean()
