from django.contrib import admin

from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
        "is_driver",
    )
    list_filter = ("is_staff", "is_superuser", "is_admin", "is_active", "is_driver")
    search_fields = ("email", "username")
