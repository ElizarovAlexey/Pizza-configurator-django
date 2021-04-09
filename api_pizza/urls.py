from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path('pizzas/', views.PizzaListView().as_view()),
    path('pizzas/<int:pk>', views.PizzaDetailView().as_view()),
    path('ingredients/', views.IngredientsListView().as_view()),
    path('doughs/', views.DoughsListView().as_view()),
    path('sizes/', views.SizesListView().as_view()),
    path('cart/', views.CartView().as_view()),
])
