from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Tag, Ingredient


def sample_user(email='test@user.com', password='testPass123'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test if creating a new user with an email is successfull"""

        # Setup
        email = "test@test.com"
        password = "testPass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # Assertions
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests if the email for a new user is normalized"""

        email = "test@DOMain.CoM"
        user = get_user_model().objects.create_user(email, "testPass123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Tests if creating users raises error"""

        # If nothing inside the with scope raises a ValueError, the test fails
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123456')

    def test_create_new_super_user(self):
        """Tests the creation of a superuser"""

        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'testPass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Tests the tag model string representation"""

        tag = Tag.objects.create(
            user=sample_user(),
            name='lacto-vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Tests the ingredient model string representation"""

        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Thicc cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
