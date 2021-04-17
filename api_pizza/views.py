from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (Size, Dough, Ingredient, Pizza, Drink, Dessert, Cart, IntermediateCart, Order)
from .serializers import (PizzasSerializer,
                          IngredientsListSerializer,
                          SizesListSerializer,
                          DoughsListSerializer,
                          CartSerializer,
                          DrinksListSerializer,
                          DessertsListSerializer,
                          OrderSerializer)


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
    """ Подробное описание одной пиццы """

    def get(self, request, pk):
        """ Вывод одной пиццы """
        try:
            pizza = Pizza.objects.get(id=pk, forSale=True)
        except Pizza.DoesNotExist:
            return Response('Pizza does not exist', status=404)

        serializer = PizzasSerializer(pizza)
        return Response(serializer.data)


class DessertListView(APIView):
    """ Вывод списка дессертов """

    def get(self, request):
        desserts = Dessert.objects.all()
        serializer = DessertsListSerializer(desserts, many=True)
        return Response(serializer.data)


class DrinkListView(APIView):
    """ Вывод списка напитков """

    def get(self, request):
        drinks = Drink.objects.all()
        serializer = DrinksListSerializer(drinks, many=True)
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


class IntermediateView(APIView):
    """ Вывод пиццы из промежуточной корзины """

    def get(self, request, pk):
        try:
            clones = IntermediateCart.objects.get(id=pk)
        except IntermediateCart.DoesNotExist:
            return Response('Not found', status=404)
        serializer = CartSerializer(clones)
        return Response(serializer.data)


class CartView(APIView):

    def get(self, request):
        """ Вывод списка товаров из корзины """

        items = Cart.objects.filter(sold=False)
        serializer = CartSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Добавление товаров в корзину """

        data = request.data

        if data['type'] == 'dessert' or data['type'] == 'drink':
            dessert_item = Cart.objects.create(name=data['name'],
                                               image=data['image'],
                                               cost=data['cost'])
            dessert_item.save()

        if data['type'] == 'pizza':
            pizza_item = Cart.objects.create(name=data['name'],
                                             image=data['image'],
                                             dough=Dough.objects.get(id=data['dough']),
                                             size=Size.objects.get(id=data['size']),
                                             cost=data['cost'])
            pizza_item.save()

            for ingredient in data['ingredients']:
                pizza_item.ingredients.add(ingredient['id'])

        return Response(status=201)

    def delete(self, request):
        """ Удаление товара из корзины """

        item_id = request.data['id']

        cart_item = Cart.objects.get(id=item_id)
        cart_item.delete()

        return Response(status=204)

    def put(self, request):
        """ Изменение количество товара в корзине """

        data = request.data

        cart_item = Cart.objects.get(id=data['id'])
        cart_item.count = data['count']
        cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(serializer.data, status=201)


class CartDetailView(APIView):

    def put(self, request, pk):
        """ Изменение пиццы в промежуточной корзине """

        item = IntermediateCart.objects.get(id=pk)
        data = request.data

        item.dough = Dough.objects.get(id=data['dough']['id'])
        item.size = Size.objects.get(id=data['size']['id'])
        item.cost = data['cost']

        item.save()

        for existing_ingredient in item.ingredients.all():
            item.ingredients.remove(existing_ingredient)

        for existing_ingredient in item.additionalIngredients.all():
            item.additionalIngredients.remove(existing_ingredient)

        for ingredient in data['ingredients']:
            item.ingredients.add(ingredient['id'])

        for ingredient in data['additionalIngredients']:
            item.additionalIngredients.add(ingredient['id'])

        serializer = CartSerializer(item)

        return Response(serializer.data, status=201)

    def post(self, request, pk):
        """ Перемещение товара из промежуточной корзины в основную """

        pizza_id = request.data['id']

        try:
            intermediate_item = IntermediateCart.objects.get(id=pizza_id)
        except Pizza.DoesNotExist:
            return Response('Item does not exist', status=404)

        cart_item = Cart.objects.create(name=intermediate_item.name + " 'индивидуальная'",
                                        image=intermediate_item.image,
                                        dough=intermediate_item.dough,
                                        size=intermediate_item.size,
                                        cost=intermediate_item.cost)
        cart_item.save()

        for ingredient in intermediate_item.ingredients.all():
            cart_item.ingredients.add(ingredient)

        for ingredient in intermediate_item.additionalIngredients.all():
            cart_item.additionalIngredients.add(ingredient)

        return Response(cart_item.id, status=201)


class OrderView(APIView):
    """ Вывод заказа """

    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data

        order_item = Order.objects.create(client_name=data['clientData']['name'],
                                          client_phone=data['clientData']['phone'],
                                          client_email=data['clientData']['email'],
                                          client_address=data['clientData']['address'],
                                          order_commentary=data['clientData']['commentary'],
                                          total_price=data['totalPrice'])

        order_item.save()

        for product in data['products']:
            order_item.order_products.add(product)
            cart_item = Cart.objects.get(id=product)
            cart_item.sold = True
            cart_item.save()

        return Response(status=201)
