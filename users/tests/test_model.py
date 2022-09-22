from django.test import TestCase
from users.models import CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        custom_user_data = {
            "username": "testuser",
            "password": "testpassword",
            "name": "Test User",
            "bio": "Hello World",
            "birth": "1999-01-04",
            "email": "test@email.com",
        }
        CustomUser.objects.create(**custom_user_data)

    def test_get_custom_user_instance_created(self):

        custom_user_instance = CustomUser.objects.get(username="testuser")
        self.assertIsInstance(custom_user_instance, CustomUser)
        self.assertEqual(CustomUser.objects.count(), 1)
