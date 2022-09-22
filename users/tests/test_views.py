import os
from rest_framework.test import APITestCase
from users.models import CustomUser
from users.views import CustomUserViewSet
from django.core.files import File
from django.conf import settings


class CustomUserViewSet(APITestCase):
    def test_can_load_custom_user_viewset(self):
        custom_user_view_set = CustomUserViewSet()
        self.assertIsInstance(custom_user_view_set, CustomUserViewSet)

    def test_can_post_custom_user_with_all_fields(self):
        url = "/api/users/"
        picture = File(open(f"{settings.BASE_DIR}/files/avatar.png", "rb"))
        custom_user_data = {
            "name": "Test User Post",
            "bio": "This is my bio...",
            "birth": "1999-10-05",
            "email": "user@email.com",
            "username": "usertwitter",
            "password": "testpassword",
            "picture": picture,
        }

        response = self.client.post(url, custom_user_data, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(response.data["name"], custom_user_data["name"])
        self.assertEqual(response.data["bio"], custom_user_data["bio"])
        self.assertEqual(response.data["birth"], custom_user_data["birth"])
        self.assertEqual(response.data["email"], custom_user_data["email"])
        self.assertEqual(response.data["username"], custom_user_data["username"])
        picture = CustomUser.objects.get(pk=response.data["id"]).picture
        self.assertIn(str(picture), response.data["picture"])
        os.remove(picture.path)

    def test_can_post_custom_user_only_with_required_data(self):
        url = "/api/users/"
        custom_user_data = {
            "name": "Test User Required",
            "birth": "1999-10-10",
            "email": "user.required@email.com",
            "username": "userrequired",
            "password": "testpasswordreq",
        }

        response = self.client.post(url, custom_user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(response.data["name"], custom_user_data["name"])
        self.assertEqual(response.data["birth"], custom_user_data["birth"])
        self.assertEqual(response.data["email"], custom_user_data["email"])
        self.assertEqual(response.data["username"], custom_user_data["username"])
        self.assertEqual(response.data["bio"], "")
        self.assertEqual(response.data["picture"], None)

    def test_cannot_post_custom_user_with_required_fields_missing(self):
        url = "/api/users/"
        custom_user_required_data_missing = {"bio": "This is an bio."}
        required_fields = ["name", "birth", "email", "username", "password"]
        response = self.client.post(url, custom_user_required_data_missing)
        self.assertEqual(response.status_code, 400)
        for field in required_fields:
            self.assertIn(field, response.json().keys())
            self.assertIn("This field is required.", response.json()[field])
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_can_update_and_partial_update_custom_user(self):

        url = "/api/users/"
        custom_user_data = {
            "name": "Test User Required",
            "birth": "1999-10-10",
            "email": "user.required@email.com",
            "username": "userrequired",
            "password": "testpasswordreq",
        }

        custom_user = CustomUser.objects.create_user(**custom_user_data)
        self.assertEqual(CustomUser.objects.count(), 1)

        custom_user_id = custom_user.id
        custom_user_update_data = {
            "name": "Test User Update",
            "bio": "This is my bio...",
            "birth": "1999-10-12",
            "email": "user.required@email.com",
            "username": "userrequired",
            "password": "testpassword",
        }

        response = self.client.put(
            f"{url}{custom_user_id}/", data=custom_user_update_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], custom_user_update_data["name"])
        self.assertEqual(response.data["birth"], custom_user_update_data["birth"])
        self.assertEqual(response.data["email"], custom_user_update_data["email"])
        self.assertEqual(response.data["username"], custom_user_update_data["username"])
        self.assertEqual(response.data["bio"], custom_user_update_data["bio"])

        custom_user_partial_update_data = {"bio": "Fixing my bio."}
        response = self.client.patch(
            f"{url}{custom_user_id}/", data=custom_user_partial_update_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["bio"], custom_user_update_data["bio"])

    def test_can_delete_custom_user(self):
        url = "/api/users/"
        custom_user_data = {
            "name": "Test User Required",
            "birth": "1999-10-10",
            "email": "user.required@email.com",
            "username": "userrequired",
            "password": "testpasswordreq",
        }
        custom_user = CustomUser.objects.create_user(**custom_user_data)
        self.assertEqual(CustomUser.objects.count(), 1)

        response = self.client.delete(f"{url}{custom_user.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_can_list_and_retrieve_custom_users(self):
        url = "/api/users/"
        custom_user_data = {
            "name": "Test User List",
            "birth": "1999-10-16",
            "email": "user.list@email.com",
            "username": "userlist",
            "password": "testpasswordlist",
        }
        custom_user = CustomUser.objects.create_user(**custom_user_data)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(custom_user.id, response.json()[0]["id"])
        self.assertEqual(5, len(response.json()[0]))

        response_retrieve = self.client.get(f"{url}{custom_user.id}/")
        self.assertEqual(response_retrieve.status_code, 200)
        self.assertEqual(custom_user.id, response_retrieve.json()["id"])
        self.assertEqual(9, len(response_retrieve.json()))
