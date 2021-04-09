from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (Size, Dough, Ingredient, Pizza, Drink, Dessert, Cart)
from .serializers import (PizzasSerializer,
                          IngredientsListSerializer,
                          SizesListSerializer,
                          DoughsListSerializer,
                          CartSerializer)


class PizzaListView(APIView):
    """ Вывод списка пицц """

    def get(self, request):
        pizzas = Pizza.objects.all()
        serializer = PizzasSerializer(pizzas, many=True)
        return Response(serializer.data)


class PizzaDetailView(APIView):
    """ Вывод одной пиццы """

    def get(self, request, pk):
        pizza = Pizza.objects.get(id=pk)
        serializer = PizzasSerializer(pizza)
        return Response(serializer.data)


class IngredientsListView(APIView):
    """ Вывод списка ингредиентов """

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientsListSerializer(ingredients, many=True)
        return Response(serializer.data)


class DoughsListView(APIView):
    """ Вывод списка типов теста """

    def get(self, request):
        doughs = Dough.objects.all()
        serializer = DoughsListSerializer(doughs, many=True)
        return Response(serializer.data)


class SizesListView(APIView):
    """ Вывод списка размеров """

    def get(self, request):
        sizes = Size.objects.all()
        serializer = SizesListSerializer(sizes, many=True)
        return Response(serializer.data)


class CartView(APIView):
    """ Вывод списка товаров из корзины """

    def get(self, request):
        items = Cart.objects.all()
        serializer = CartSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        new_item = Cart.objects.create(name=data['name'],
                                       image=data['image'],
                                       dough=Dough.objects.get(id=data['dough']),
                                       size=Size.objects.get(id=data['size']),
                                       cost=data['cost'])
        new_item.save()

        for ingredient in data['ingredients']:
            ingredient_obj = Ingredient.objects.get(value=ingredient['value'],
                                                    cost=ingredient['cost'])
            new_item.ingredients.add(ingredient_obj)

        serializer = CartSerializer(new_item)

        return Response(serializer.data)
