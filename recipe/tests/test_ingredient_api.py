from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientstApiTests(TestCase):
  """Test the publically available ingredients API"""

  def setUp(self):
    self.client = APIClient()

  def test_login_required(self):
    """Login is required to access endpoint"""
    res = self.client.get(INGREDIENT_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
  """Test Inngredients can be retrieved by authorized user"""

  def setUp(self):
    self.client = APIClient()
    self.user = get_user_model().objects.create_user('test@gmail.com', 'testpass123')

    self.client.force_authenticate(self.user)

  def test_retrieved_ingredient_list(self):
    """Test retrieving list of ingredients"""
    Ingredient.objects.create(user=self.user, name='Kale')
    Ingredient.objects.create(user=self.user, name='Salt')

    res = self.client.get(INGREDIENT_URL)

    ingredients = Ingredient.objects.all().order_by('-name')
    serializer = IngredientSerializer(ingredients, many=True)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)

  def test_ingredients_limited_to_authenticated_user(self):
    """Test that the ingrdients are returned to authenticacte user"""
    user2 = get_user_model().objects.create_user('new@gmail.com', 'new1234')

    Ingredient.objects.create(user=user2, name='Vinegar')
    ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

    res = self.client.get(INGREDIENT_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]['name'], ingredient.name) 