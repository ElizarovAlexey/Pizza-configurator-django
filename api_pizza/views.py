from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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

    def get(self, request):
        """ Вывод списка пицц """
        try:
            pizzas = Pizza.objects.filter(forSale=True)
        except Pizza.DoesNotExist:
            return Response('Pizzas does not exist', status=404)

        serializer = PizzasSerializer(pizzas, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """ Добавление пиццы в промежуточную корзину """

        pizza_id = request.data['id']

        try:
            pizza_clone = Pizza.objects.get(id=pizza_id)
        except Pizza.DoesNotExist:
            return Response(f'Pizza with id {pizza_id} does not exist', status=404)

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
        except Pizza.objects.get(id=pk, forSale=True).DoesNotExist:
            return Response(f'Pizza with id {pk} does not exist', status=404)

        serializer = PizzasSerializer(pizza)
        return Response(serializer.data, status=200)


class DessertListView(APIView):
    """ Вывод списка дессертов """

    def get(self, request):
        try:
            desserts = Dessert.objects.all()
        except Dessert.DoesNotExist:
            return Response('Desserts does not exist', status=404)

        serializer = DessertsListSerializer(desserts, many=True)
        return Response(serializer.data, status=200)


class DrinkListView(APIView):
    """ Вывод списка напитков """

    def get(self, request):
        try:
            drinks = Drink.objects.all()
        except Drink.DoesNotExist:
            return Response('Drinks does not exist', status=404)

        serializer = DrinksListSerializer(drinks, many=True)
        return Response(serializer.data)


class IngredientsListView(APIView):
    """ Вывод списка ингредиентов """

    def get(self, request):
        try:
            ingredients = Ingredient.objects.all()
        except Ingredient.DoesNotExist:
            return Response('Ingredients does not exist', status=404)

        serializer = IngredientsListSerializer(ingredients, many=True)
        return Response(serializer.data, status=200)


class DoughsListView(APIView):
    """ Вывод списка типов теста """

    def get(self, request):
        try:
            doughs = Dough.objects.all()
        except Dough.DoesNotExist:
            return Response('Dough does not exist', status=404)

        serializer = DoughsListSerializer(doughs, many=True)
        return Response(serializer.data, status=200)


class SizesListView(APIView):
    """ Вывод списка размеров """

    def get(self, request):
        try:
            sizes = Size.objects.all()
        except Size.DoesNotExist:
            return Response('Sizes does not exist', status=404)

        serializer = SizesListSerializer(sizes, many=True)
        return Response(serializer.data, status=200)


class IntermediateView(APIView):

    def get(self, request, pk):
        """ Вывод пиццы из промежуточной корзины """

        try:
            clones = IntermediateCart.objects.get(id=pk)
        except IntermediateCart.DoesNotExist:
            return Response(f'Intermediate cart object with id {pk} does not exist', status=404)

        serializer = CartSerializer(clones)
        return Response(serializer.data, status=200)


class CartView(APIView):

    def get(self, request):
        """ Вывод списка товаров из корзины """

        try:
            items = Cart.objects.filter(sold=False)
        except Cart.DoesNotExist:
            return Response('Cart item does not exist', status=404)

        serializer = CartSerializer(items, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """ Добавление товаров в корзину """

        data = request.data

        if data['type'] == '':
            return Response('The necessary information is not provided', status=400)

        if data['type'] == 'dessert':
            try:
                dessert_item = Dessert.objects.get(id=data['id'])
            except Dessert.DoesNotExist:
                return Response(f'Dessert does not exist', status=404)

            try:
                cart_object = Cart.objects.get(name=dessert_item.name, sold=False)
            except Cart.DoesNotExist:
                cart_item = Cart.objects.create(name=dessert_item.name,
                                                image=dessert_item.image,
                                                cost=dessert_item.cost,
                                                discount=dessert_item.discount)
                cart_item.save()

                return Response(status=201)

            if cart_object in Cart.objects.all():
                cart_object.count += 1
                cart_object.save()
                return Response(status=202)

        if data['type'] == 'drink':
            try:
                drink_item = Drink.objects.get(id=data['id'])
            except Dessert.DoesNotExist:
                return Response(f'Drink does not exist', status=404)

            try:
                cart_object = Cart.objects.get(name=drink_item.name, sold=False)
            except Cart.DoesNotExist:
                cart_item = Cart.objects.create(name=drink_item.name,
                                                image=drink_item.image,
                                                cost=drink_item.cost,
                                                discount=drink_item.discount)
                cart_item.save()

                return Response(status=201)

            if cart_object in Cart.objects.all():
                cart_object.count += 1
                cart_object.save()
                return Response(status=202)

        if data['type'] == 'pizza':
            try:
                pizza_item = Pizza.objects.get(id=data['id'])
            except Dessert.DoesNotExist:
                return Response(f'Pizza does not exist', status=404)

            if data['cost'] is None:
                return Response('The necessary information is not provided', status=400)

            try:
                cart_object = Cart.objects.get(name=pizza_item.name, sold=False)
            except Cart.DoesNotExist:
                cart_item = Cart.objects.create(name=pizza_item.name,
                                                image=pizza_item.image,
                                                dough=pizza_item.dough,
                                                size=pizza_item.size,
                                                cost=data['cost'],
                                                discount=pizza_item.discount)
                cart_item.save()

                for ingredient in pizza_item.ingredients.all():
                    cart_item.ingredients.add(ingredient)

                return Response(status=201)

            if cart_object in Cart.objects.all():
                cart_object.count += 1
                cart_object.save()
                return Response(status=202)

    def put(self, request):
        """ Изменение количество товара в корзине """

        data = request.data
        item_id = data['id']

        try:
            cart_item = Cart.objects.get(id=item_id)
        except Cart.DoesNotExist:
            return Response(f'Cart object with id {item_id} does not exist', status=404)

        cart_item.count = data['count']
        cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(serializer.data, status=202)

    def delete(self, request):
        """ Удаление товара из корзины """

        item_id = request.data['id']

        try:
            cart_item = Cart.objects.get(id=item_id)
        except Cart.DoesNotExist:
            return Response(f'Cart object with id {item_id} does not exist', status=404)
        cart_item.delete()

        return Response(status=202)


class CartDetailView(APIView):

    def put(self, request, pk):
        """ Изменение пиццы в промежуточной корзине """

        data = request.data

        try:
            intermediate_item = IntermediateCart.objects.get(id=pk)
        except IntermediateCart.DoesNotExist:
            return Response(f'Cart object with id {pk} does not exist', status=404)

        intermediate_item.dough = Dough.objects.get(id=data['dough'])
        intermediate_item.size = Size.objects.get(id=data['size'])
        intermediate_item.cost = data['cost']

        intermediate_item.save()

        for existing_ingredient in intermediate_item.ingredients.all():
            intermediate_item.ingredients.remove(existing_ingredient)

        for existing_ingredient in intermediate_item.additionalIngredients.all():
            intermediate_item.additionalIngredients.remove(existing_ingredient)

        for ingredient in data['ingredients']:
            intermediate_item.ingredients.add(ingredient['id'])

        for ingredient in data['additionalIngredients']:
            intermediate_item.additionalIngredients.add(ingredient['id'])

        serializer = CartSerializer(intermediate_item)

        return Response(serializer.data, status=202)

    def post(self, request, pk):
        """ Перемещение товара из промежуточной корзины в основную """

        pizza_id = request.data['id']

        try:
            intermediate_item = IntermediateCart.objects.get(id=pizza_id)
        except IntermediateCart.objects.get(id=pizza_id).DoesNotExist:
            return Response(f'Intermediate cart with id {pizza_id} does not exist', status=404)

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

    def get(self, request):
        """ Вывод заказов """

        try:
            order = Order.objects.all()
        except Order.DoesNotExist:
            return Response('Orders does not exist', status=404)

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """ Добавление заказа """

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
