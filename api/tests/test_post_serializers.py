from django.test import TestCase
from django.conf import settings
from django.core.files import File
from api.serializers.post import PostCreateOrUpdateSerializer


class PostCreateOrUpdateSerializerTestCase(TestCase):
    def test_can_load_post_create_or_update_serializer(self):
        post_create_or_update_serializer = PostCreateOrUpdateSerializer()
        self.assertIsInstance(
            post_create_or_update_serializer, PostCreateOrUpdateSerializer
        )

    def test_cannot_represent_post_required_field_missing(self):
        post_create_or_update_serializer = PostCreateOrUpdateSerializer(data={})
        self.assertFalse(post_create_or_update_serializer.is_valid())
        self.assertEqual(
            post_create_or_update_serializer.errors,
            {"content": ["This field is required."]},
        )

    def test_content_field_cannot_accept_more_than_140_characters(self):
        post_create_or_update_serializer = PostCreateOrUpdateSerializer(
            data={"content": "a" * 141}
        )
        self.assertFalse(post_create_or_update_serializer.is_valid())
        self.assertEqual(
            post_create_or_update_serializer.errors,
            {"content": ["Ensure this field has no more than 140 characters."]},
        )

    def test_can_represent_post_with_all_fields(self):
        picture = File(open(f"{settings.BASE_DIR}/files/avatar.png", "rb"))
        post_create_or_update_serializer = PostCreateOrUpdateSerializer(
            data={"content": "a" * 140, "picture": picture}
        )
        self.assertTrue(post_create_or_update_serializer.is_valid())

    def test_cannot_represent_post_with_invalid_picture_format(self):
        picture = File(open(f"{settings.BASE_DIR}/files/file.txt", "rb"))
        post_create_or_update_serializer = PostCreateOrUpdateSerializer(
            data={"content": "a" * 140, "picture": picture}
        )
        self.assertFalse(post_create_or_update_serializer.is_valid())
        self.assertIn("picture", post_create_or_update_serializer.errors)