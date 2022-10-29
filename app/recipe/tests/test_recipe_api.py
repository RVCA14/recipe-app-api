"""
Test for Recipe APIs.
"""


from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework_test import APIClient

from core import Recipe

from recipe.serializer import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """Create and return a Sample Recipe"""
    defaults = {
        'title': 'Sample title',
        'time_minutes': 34,
        'price': Decimal('5.52'),
        'link':'https://example.com/recipe.pdf'
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

class PublicRecipeAPITests(TestCase):
    """Test unauthenticate API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_AUTHORIZATION)

class PrivateRecipeAPITests(TestCase):
    """Test authenticate API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'test1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited by the authenticated user"""
        other_user = get_user_model().objects.create_user(
            'another-user@example.com',
            "test1234"
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer= RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_ok)
        self.assertEqual(res.data, serializer.data)


# Create your tests here.
