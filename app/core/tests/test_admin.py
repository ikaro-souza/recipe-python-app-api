from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Function that is ran before every test"""

        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="testPass123"
        )

        # a mock client to access the project web pages
        self.client = Client()
        # logs a user in with a django authentication
        self.client.force_login(self.admin_user)

        # a regular user to be listed on the admin web page
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="testPass123",
            name="Lorem Ipsum Boi"
        )

    def test_users_listed(self):
        """Tests if users are listed on admin page"""

        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Tests if the user change page works"""

        url = reverse("admin:core_user_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Tests if the user creation page works"""

        url = reverse("admin:core_user_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
