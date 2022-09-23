import os
from urllib import response
from wsgiref import headers
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from users.models import CustomUser
from django.core.files import File
from django.conf import settings
from api.views.post import PostViewSet
from api.models.post import Post


class PostViewSetTestCase(APITestCase):
    def setUp(self):
        custom_user_data = {
            "name": "Test User Token",
            "birth": "2018-08-01",
            "email": "user@email.com",
            "username": "usertoken",
            "password": "my*pass",
        }
        self.custom_user = CustomUser.objects.create_user(**custom_user_data)

    def test_can_load_post_viewset(self):
        post_view_set = PostViewSet()
        self.assertIsInstance(post_view_set, PostViewSet)

    def test_cannot_save_post_without_authentication(self):

        post_data = {
            "content": "This is a post content!",
            "picture": File(open(f"{settings.BASE_DIR}/files/avatar.png", "rb")),
        }
        response = self.client.post("/api/posts/", post_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_can_custom_user_logged_save_post(self):

        url = "/api/login/"
        request_data = {"username": "usertoken", "password": "my*pass"}
        response = self.client.post(url, request_data)
        acess_token = response.json()["access"]

        post_data = {
            "content": "This is a post content!",
            "picture": File(open(f"{settings.BASE_DIR}/files/avatar.png", "rb")),
        }
        response_post = self.client.post(
            "/api/posts/",
            post_data,
            format="multipart",
            **{"HTTP_AUTHORIZATION": f"Bearer {acess_token}"},
        )

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_post.json()["content"], post_data["content"])
        self.assertEqual(response_post.json()["author"], self.custom_user.id)
        picture = Post.objects.get(pk=response_post.json()["id"]).picture
        self.assertIn(str(picture), response_post.json()["picture"])
        os.remove(picture.path)
