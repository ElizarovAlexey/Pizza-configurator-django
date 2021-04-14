from rest_framework import serializers
from .models import Pizza, Dough, Size, Ingredient, Cart, Dessert, Drink


class IngredientsListSerializer(serializers.ModelSerializer):
    """ Вывод списка пицц """

    class Meta:
        model = Ingredient
        fields = '__all__'


class DoughsListSerializer(serializers.ModelSerializer):
    """ Вывод типов теста """

    class Meta:
        model = Dough
        fields = '__all__'


class SizesListSerializer(serializers.ModelSerializer):
    """ Вывод списка размеров пиццы """

    class Meta:
        model = Size
        fields = '__all__'


class PizzasSerializer(serializers.ModelSerializer):
    """ Вывод списка пицц """

    dough = DoughsListSerializer()
    size = SizesListSerializer()
    ingredients = IngredientsListSerializer(many=True)

    class Meta:
        model = Pizza
        fields = '__all__'


class DessertsListSerializer(serializers.ModelSerializer):
    """ Вывод списка дессертов """

    class Meta:
        model = Dessert
        fields = '__all__'


class DrinksListSerializer(serializers.ModelSerializer):
    """ Вывод списка напитков """

    class Meta:
        model = Dessert
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    """ Вывод списка товаров из корзины """

    size = SizesListSerializer()
    dough = DoughsListSerializer()
    ingredients = IngredientsListSerializer(many=True)
    additionalIngredients = IngredientsListSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
