from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import (Size, Dough, Ingredient, Pizza, Drink, Dessert, Cart, IntermediateCart)
from .serializers import (PizzasSerializer,
                          IngredientsListSerializer,
                          SizesListSerializer,
                          DoughsListSerializer,
                          CartSerializer)


class PizzaListView(APIView):
    """ Вывод списка пицц """

    def get(self, request):
        pizzas = Pizza.objects.filter(forSale=True)
        serializer = PizzasSerializer(pizzas, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Добавление пиццы в промежуточную корзину """

        pizza_id = request.data
        try:
            pizza_clone = Pizza.objects.get(id=pizza_id['id'])
        except Pizza.DoesNotExist:
            return Response('Pizza does not exist', status=404)
        item = IntermediateCart.objects.create(name=pizza_clone.name,
                                               image=pizza_clone.image,
                                               dough=pizza_clone.dough,
                                               size=pizza_clone.size,
                                               cost=pizza_clone.cost)
        item.save()

        for ingredient in pizza_clone.ingredients.all():
            item.ingredients.add(ingredient)

        for ingredient in Ingredient.objects.all():
            item.additionalIngredients.add(ingredient)

        return Response(item.id, status=201)


class PizzaDetailView(APIView):
    """ Вывод одной пиццы """

    def get(self, request, pk):
        try:
            pizza = Pizza.objects.get(id=pk, forSale=True)
        except Pizza.DoesNotExist:
            return Response('Pizza does not exist', status=404)

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


class PizzaCloneView(APIView):
    """ Клонирование базовой пиццы """

    def get(self, request, pk):
        try:
            clones = IntermediateCart.objects.get(id=pk)
        except IntermediateCart.DoesNotExist:
            return Response('Not found', status=404)
        serializer = CartSerializer(clones)
        return Response(serializer.data)

    # def post(self, request):
    #     pizza_id = request.data
    #     pizza_clone = Pizza.objects.get(id=pizza_id['id'])
    #     item = IntermediateCart.objects.create(id=pizza_clone.id,
    #                                            name=pizza_clone.name,
    #                                            image=pizza_clone.image,
    #                                            dough=pizza_clone.dough,
    #                                            size=pizza_clone.size,
    #                                            cost=pizza_clone.cost)
    #     item.save()
    #
    #     for ingredient in pizza_clone.ingredients.all():
    #         item.ingredients.add(ingredient)
    #
    #     for ingredient in Ingredient.objects.all():
    #         item.additionalIngredients.add(ingredient)
    #
    #     return Response({"id": pizza_clone.id}, status=201)


class CartView(APIView):

    def get(self, request):
        """ Вывод списка товаров из корзины """
        items = Cart.objects.all()
        serializer = CartSerializer(items, many=True)
        return Response(serializer.data)
