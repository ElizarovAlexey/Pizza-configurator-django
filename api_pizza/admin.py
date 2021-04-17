from django.contrib import admin

from .models import Pizza, Ingredient, Dough, Size, Cart, IntermediateCart, Drink, Dessert, Order

admin.site.register(Ingredient)
admin.site.register(Dough)
admin.site.register(Size)
admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(IntermediateCart)
admin.site.register(Dessert)
admin.site.register(Drink)
admin.site.register(Order)
