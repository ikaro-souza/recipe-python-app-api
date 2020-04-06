from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipes.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipes:ingredient-list')


def create_ingredient(user, ingredient_name):
    return Ingredient.objects.create(user=user, name=ingredient_name)


class PublicIngredientsApiTests(TestCase):
    """Tests the ingredients api public methods"""

    def setUp(self):
        self.client = APIClient()

    def test_is_authentication_required(self):
        """Tests whether the user must be authenticated to fetch ingredients"""

        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Tests the ingredients api private methods"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@user.com',
            password='testPass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_fetch_ingredient_list(self):
        """Tests fetching a list of ingredients"""

        create_ingredient(self.user, 'Thicc cucumber')
        create_ingredient(self.user, 'Normal cucumber')
        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_fetching_authenticated_user_ingredients_only(self):
        """
        Tests whether only the ingredients of the authenticated
        are being fetched
        """

        user2 = get_user_model().objects.create_user(
            email='test2@user.com',
            password='testPass123'
        )
        create_ingredient(user2, 'Coconut')
        ingredient = create_ingredient(self.user, 'thicc cucumber')
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)

    def test_create_ingredient_successfull(self):
        """Tests the successfull creation of a ingredient"""

        payload = {'name': 'garbage'}
        response = self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_ingredient_invalid_payload(self):
        """Tests the creation of a ingredient with invalid payload"""

        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
