from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """test the publicly available api test"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateIngredientApiTest(TestCase):
    """test the private ingredients API test"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredient_list(self):
        """test retrieving a list of ingredient"""
        Ingredient.objects.create(user=self.user, name='kaku')
        Ingredient.objects.create(user=self.user, name='momu')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """test that ingredients for the authenticated user returend"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'test2pass'
        )
        Ingredient.objects.create(user=user2, name='termname')
        ingredient = Ingredient.objects.create(user=self.user, name='superduper')

        res = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)