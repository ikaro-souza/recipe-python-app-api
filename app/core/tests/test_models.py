from django.test import TestCase
from django.contrib.auth import get_user_model


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
