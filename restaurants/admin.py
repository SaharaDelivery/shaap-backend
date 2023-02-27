from django.contrib import admin

from restaurants.models import Cuisine, Menu, MenuItem, Restaurant

admin.site.register(Restaurant)
admin.site.register(Cuisine)
admin.site.register(Menu)
admin.site.register(MenuItem)