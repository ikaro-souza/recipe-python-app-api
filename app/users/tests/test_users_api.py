from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users:create')
USER_TOKEN_URL = reverse('users:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    """Tests the users api public methods"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Tests if creating a user with valid payload is successfull"""

        payload = {
            'email': 'test@user.com',
            'password': 'testUser123',
            'name': 'Big Docker Guy'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Tests whether a user exists"""

        payload = {
            'email': 'test@user.com',
            'password': 'testUser123'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Tests if a given password is at least 6 characters long"""

        payload = {
            'email': 'test@user.com',
            'password': '123',
            'name': 'Big Docker Guy'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_user_token(self):
        """Tests if a token is successfully created"""

        payload = {
            'email': 'test@user.com',
            'password': 'testUser123',
        }
        create_user(**payload)
        response = self.client.post(USER_TOKEN_URL, {
            'email': payload['email'], 
            'password': payload['password'],
        })

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_token_invalid_credentials(self):
        """Tests if token is not createad when invalid credentials are given"""

        email = 'test@test.com'
        payload = {
            'email': email,
            'password': 'wrong',
        }
        create_user(email=email, password='testpass')
        response = self.client.post(USER_TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_token_missing_field(self):
        """Tests if email and password are required"""

        payload_no_email = {'email': '', 'password': 'wrong'}
        response_no_email = self.client.post(USER_TOKEN_URL, payload_no_email)

        payload_no_password = {'email': 'test@test.com', 'password': ''}
        response_no_password = self.client.post(
            USER_TOKEN_URL, payload_no_password
        )

        self.assertNotIn('token', response_no_email.data)
        self.assertEqual(
            response_no_email.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertNotIn('token', response_no_password.data)
        self.assertEqual(
            response_no_password.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_user_token_user_not_found(self):
        """Tests if token is not created to a non-existent user"""

        payload = {
            'email': 'test@test.com',
            'password': 'testpass'
        }
        response = self.client.post(USER_TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
