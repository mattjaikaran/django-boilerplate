from django.test import TestCase
from .models import CustomUser


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            first_name="John",
            last_name="Doe",
            password="testpassword",
        )

    def test_full_name_property(self):
        user = CustomUser.objects.get(username="testuser")
        full_name = user.full_name
        self.assertEqual(full_name, "John Doe")

    def test_email_unique_constraint(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                username="anotheruser",
                email="testuser@example.com",
                first_name="Jane",
                last_name="Smith",
                password="anotherpassword",
            )

    def test_username_unique_constraint(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                username="testuser",
                email="anotheruser@example.com",
                first_name="Alice",
                last_name="Johnson",
                password="anotherpassword",
            )
