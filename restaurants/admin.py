from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from restaurants.models import Cuisine, Menu, MenuItem, Restaurant, RestaurantStaff

admin.site.register(RestaurantStaff, SimpleHistoryAdmin)
admin.site.register(Restaurant, SimpleHistoryAdmin)
admin.site.register(Cuisine, SimpleHistoryAdmin)
admin.site.register(Menu, SimpleHistoryAdmin)
admin.site.register(MenuItem, SimpleHistoryAdmin)