from rest_framework.serializers import ModelSerializer
from api.models.post import Post
from users.serializers import CustomUserPostListSerializer, CustomUserRetrieveSerializer


class PostCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "content", "picture"]
        extra_kwargs = {"author": {"read_only": True}}


class PostListSerializer(ModelSerializer):

    author = CustomUserPostListSerializer()

    class Meta:
        model = Post
        fields = ["id", "author", "content", "picture"]


class PostRetrieveSerializer(ModelSerializer):

    author = CustomUserRetrieveSerializer()

    class Meta:
        model = Post
        fields = "__all__"
