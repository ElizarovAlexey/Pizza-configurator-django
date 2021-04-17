from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path('pizzas/', views.PizzaListView().as_view(), name='home_page'),
    path('pizzas/<int:pk>', views.PizzaDetailView().as_view()),
    path('ingredients/', views.IngredientsListView().as_view()),
    path('doughs/', views.DoughsListView().as_view()),
    path('sizes/', views.SizesListView().as_view()),
    path('cart/', views.CartView().as_view()),
    path('cart/<int:pk>', views.CartDetailView().as_view()),
    path('intermediate/<int:pk>', views.IntermediateView().as_view()),
    path('drinks/', views.DrinkListView().as_view()),
    path('desserts/', views.DessertListView().as_view()),
    path('orders/', views.OrderView().as_view()),
])
