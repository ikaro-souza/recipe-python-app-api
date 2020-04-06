from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipes.serializers import TagSerializer


TAGS_URL = reverse('recipes:tag-list')


class PublicTagsApisTests(TestCase):
    """Tests the tags api public methods"""

    def setUp(self):
        self.client = APIClient()

    def test_authentications_is_required(self):
        """Tests whether the user must be authenticated to fetch recipe tags"""

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Tests the tags api private methods"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@user.com',
            password='testPass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_tags(self):
        """Tests retrieving tags"""

        Tag.objects.create(user=self.user, name='lactopurga-vegan')
        Tag.objects.create(user=self.user, name='dessert')

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Tests if tags returned are for the authenticated user"""

        user2 = get_user_model().objects.create_user(
            email='test@test2.com',
            password='testpass213',
            name='other boi'
        )
        Tag.objects.create(user=user2, name='fruits')
        user1_tag = Tag.objects.create(user=self.user, name='pasta')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], user1_tag.name)

    def test_create_tag_successfull(self):
        """Tests creating a new tag"""

        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user, name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Tests the creation of a tag with invalid payload"""

        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
