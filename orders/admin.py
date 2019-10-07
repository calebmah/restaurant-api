from django.contrib import admin

from .models import MenuItems, Orders, Restaurants

# Register your models here.

admin.site.register(Orders)
admin.site.register(Restaurants)
admin.site.register(MenuItems)
