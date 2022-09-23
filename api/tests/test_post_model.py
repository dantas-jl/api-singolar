from django.test import TestCase
from django.conf import settings
from django.core.files import File
from users.models import CustomUser
from api.models.post import Post


class PostTestCase(TestCase):
    def setUp(self):
        custom_user_data = {
            "username": "testuser",
            "password": "testpassword",
            "name": "Test User",
            "bio": "Hello World",
            "birth": "1999-01-04",
            "email": "test@email.com",
        }
        self.custom_user = CustomUser.objects.create(**custom_user_data)
        post_data = {
            "author": self.custom_user,
            "content": "My first post!",
        }
        Post.objects.create(**post_data)

    def test_get_post_instance_created(self):

        post_instance_created = Post.objects.get(author=self.custom_user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertIsInstance(post_instance_created, Post)
