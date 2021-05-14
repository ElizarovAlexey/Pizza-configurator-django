from api_pizza.models import Pizza

from mixer.backend.django import mixer

from django.test import TestCase
from rest_framework.test import APIClient


class TestPizzasApiViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_pizza_list(self):
        pizza = mixer.blend(Pizza, name='4 сыра')

        response = self.client.get('api/v1/pizzas/')

        assert response.json is not None
        assert response.status_code == 200
