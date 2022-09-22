import os
from django.test import TestCase
from django.conf import settings
from django.core.files import File
from users.models import CustomUser
from users.serializers import (
    CustomUserCreateOrUpdateSerializer,
    CustomUserListSerializer,
    CustomUserRetrieveSerializer,
)


class CustomUserCreateUpdateSerializerTestCase(TestCase):
    def test_can_load_custom_user_create_or_update_serializer(self):

        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer()
        self.assertIsInstance(
            custom_user_create_or_update_serializer, CustomUserCreateOrUpdateSerializer
        )

    def test_required_fields(self):
        custom_user_data = {}
        required_fields = ["name", "birth", "email", "username", "password"]
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )
        self.assertFalse(custom_user_create_or_update_serializer.is_valid())
        for field in required_fields:
            self.assertIn(field, custom_user_create_or_update_serializer.errors)
            self.assertDictContainsSubset(
                {field: ["This field is required."]},
                custom_user_create_or_update_serializer.errors,
            )

    def test_cannot_save_custom_user_with_required_field_missing(self):
        custom_user_data = {
            "name": "Test User",
            "email": "test@email.com",
            "username": "testuser",
            "password": "testpassword",
        }
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )
        self.assertFalse(custom_user_create_or_update_serializer.is_valid())
        with self.assertRaises(AssertionError):
            custom_user_create_or_update_serializer.save()
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_can_save_custom_user_with_only_required_fields(self):
        custom_user_data = {
            "name": "Test User",
            "birth": "1999-01-04",
            "email": "test@email.com",
            "username": "testuser",
            "password": "testpassword",
        }
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )
        self.assertTrue(custom_user_create_or_update_serializer.is_valid())

        custom_user_created = custom_user_create_or_update_serializer.save()
        self.assertIsInstance(custom_user_created, CustomUser)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_are_optional_fields_in_custom_user_create_serializer(self):
        optional_fields = ["bio", "picture"]
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data={}
        )
        for field in optional_fields:
            self.assertIn(field, custom_user_create_or_update_serializer.fields.fields)

    def test_can_save_custom_user_with_all_fields(self):

        picture = File(open(f"{settings.BASE_DIR}/files/avatar.png", "rb"))
        custom_user_data = {
            "name": "Test User",
            "bio": "This is a bio...",
            "birth": "1999-01-04",
            "email": "test@email.com",
            "username": "testuser",
            "password": "testpassword",
            "picture": picture,
        }
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )

        self.assertTrue(custom_user_create_or_update_serializer.is_valid())
        custom_user_created = custom_user_create_or_update_serializer.save()
        self.assertIsInstance(custom_user_created, CustomUser)
        self.assertEqual(custom_user_created.name, custom_user_data["name"])
        self.assertEqual(custom_user_created.bio, custom_user_data["bio"])
        self.assertEqual(
            custom_user_created.birth.strftime("%Y-%m-%d"), custom_user_data["birth"]
        )
        self.assertEqual(custom_user_created.email, custom_user_data["email"])
        self.assertEqual(custom_user_created.username, custom_user_data["username"])
        self.assertEqual(custom_user_created.password, custom_user_data["password"])
        self.assertEqual(custom_user_created.picture.size, picture.size)
        os.remove(custom_user_created.picture.path)

    def test_cannot_save_custom_user_with_invalid_picture_format(self):

        text_file = File(open(f"{settings.BASE_DIR}/files/file.txt", "rb"))
        custom_user_data = {
            "name": "Test User",
            "bio": "This is a bio...",
            "birth": "1999-01-04",
            "email": "test@email.com",
            "username": "testuser",
            "password": "testpassword",
            "picture": text_file,
        }
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )

        self.assertFalse(custom_user_create_or_update_serializer.is_valid())
        self.assertIn("picture", custom_user_create_or_update_serializer.errors)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_can_custom_user_update(self):

        custom_user_data = {
            "name": "Test User",
            "bio": "This is a bio...",
            "birth": "1999-01-04",
            "email": "test@email.com",
            "username": "testuser",
            "password": "testpassword",
        }
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )

        self.assertTrue(custom_user_create_or_update_serializer.is_valid())
        custom_user_created = custom_user_create_or_update_serializer.save()
        self.assertIsInstance(custom_user_created, CustomUser)

        new_custom_user_data = {
            "name": "New Test User",
            "bio": "This is a new bio...",
            "birth": "1999-01-05",
            "email": "test_hi@email.com",
            "username": "testusernew",
            "password": "testpasswordnew",
        }

        custom_user_update_serializer = CustomUserCreateOrUpdateSerializer(
            custom_user_created, data=new_custom_user_data, partial=False
        )
        self.assertTrue(custom_user_update_serializer.is_valid())
        custom_user_updated = custom_user_update_serializer.save()
        self.assertIsInstance(custom_user_updated, CustomUser)
        self.assertEqual(custom_user_updated.name, new_custom_user_data["name"])
        self.assertEqual(custom_user_updated.bio, new_custom_user_data["bio"])
        self.assertEqual(
            custom_user_updated.birth.strftime("%Y-%m-%d"),
            new_custom_user_data["birth"],
        )
        self.assertEqual(custom_user_updated.email, new_custom_user_data["email"])
        self.assertEqual(custom_user_updated.username, new_custom_user_data["username"])
        self.assertEqual(custom_user_updated.password, new_custom_user_data["password"])
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_can_custom_user_partial_update(self):

        custom_user_data = {
            "name": "Test User Partial",
            "bio": "This is a bio partial...",
            "birth": "1999-01-07",
            "email": "testpartial@email.com",
            "username": "testuserpartial",
            "password": "testpasswordpartial",
        }
        custom_user_create_or_update_serializer = CustomUserCreateOrUpdateSerializer(
            data=custom_user_data
        )

        self.assertTrue(custom_user_create_or_update_serializer.is_valid())
        custom_user_created = custom_user_create_or_update_serializer.save()
        self.assertIsInstance(custom_user_created, CustomUser)

        new_custom_user_data_patial = {"name": "New Test User"}

        custom_user_update_serializer = CustomUserCreateOrUpdateSerializer(
            custom_user_created, data=new_custom_user_data_patial, partial=True
        )
        self.assertTrue(custom_user_update_serializer.is_valid())
        custom_user_updated = custom_user_update_serializer.save()
        self.assertIsInstance(custom_user_updated, CustomUser)
        self.assertEqual(custom_user_updated.name, new_custom_user_data_patial["name"])
        self.assertEqual(custom_user_updated.bio, custom_user_data["bio"])
        self.assertEqual(
            custom_user_updated.birth.strftime("%Y-%m-%d"), custom_user_data["birth"]
        )
        self.assertEqual(custom_user_updated.email, custom_user_data["email"])
        self.assertEqual(custom_user_updated.username, custom_user_data["username"])
        self.assertEqual(custom_user_updated.password, custom_user_data["password"])
        self.assertEqual(CustomUser.objects.count(), 1)


class CustomUserListAndRetrieveSerializerTestCase(TestCase):
    def setUp(self):
        custom_user_data = {
            "name": "Test User List",
            "bio": "This is a bio list...",
            "birth": "1999-01-08",
            "email": "testlist@email.com",
            "username": "testuserlist",
            "password": "testpasswordlist",
        }
        self.custom_user = CustomUser.objects.create(**custom_user_data)

    def test_can_load_custom_user_list_serializer(self):

        custom_user_list_serializer = CustomUserListSerializer()
        self.assertIsInstance(custom_user_list_serializer, CustomUserListSerializer)

    def test_custom_user_list_serializer_can_be_used_to_represent(self):

        custom_user_list_serializer = CustomUserListSerializer(self.custom_user)
        self.assertEqual(custom_user_list_serializer.data["id"], self.custom_user.id)
        self.assertEqual(
            custom_user_list_serializer.data["name"], self.custom_user.name
        )
        self.assertEqual(custom_user_list_serializer.data["bio"], self.custom_user.bio)
        self.assertEqual(5, len(custom_user_list_serializer.data))

    def test_can_load_custom_user_retrieve_serializer(self):

        custom_user_retrieve_serializer = CustomUserRetrieveSerializer()
        self.assertIsInstance(
            custom_user_retrieve_serializer, CustomUserRetrieveSerializer
        )

    def test_custom_user_retrieve_serializer_can_be_used_to_represent(self):

        custom_user_retrieve_serializer = CustomUserRetrieveSerializer(self.custom_user)
        self.assertEqual(
            custom_user_retrieve_serializer.data["id"], self.custom_user.id
        )
        self.assertEqual(
            custom_user_retrieve_serializer.data["name"], self.custom_user.name
        )
        self.assertEqual(
            custom_user_retrieve_serializer.data["bio"], self.custom_user.bio
        )
        self.assertEqual(9, len(custom_user_retrieve_serializer.data))
