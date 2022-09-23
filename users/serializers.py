from urllib import request
from rest_framework.serializers import ModelSerializer
from users.models import CustomUser


class CustomUserCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "bio",
            "picture",
            "birth",
            "email",
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserListSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "name", "bio", "picture"]


class CustomUserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "bio",
            "picture",
            "birth",
            "email",
            "username",
            "created_at",
            "updated_at",
        ]


class CustomUserShortSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "name", "picture"]
