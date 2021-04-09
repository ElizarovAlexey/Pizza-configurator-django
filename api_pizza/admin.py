from django.contrib import admin

from .models import Pizza, Ingredient, Dough, Size, Cart

admin.site.register(Ingredient)
admin.site.register(Dough)
admin.site.register(Size)
admin.site.register(Pizza)
admin.site.register(Cart)
