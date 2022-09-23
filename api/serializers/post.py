from rest_framework.serializers import ModelSerializer, CharField
from api.models.post import Post
from users.serializers import CustomUserShortSerializer, CustomUserRetrieveSerializer


class PostCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "content", "picture"]
        extra_kwargs = {"author": {"read_only": True}}


class PostListSerializer(ModelSerializer):

    author = CustomUserShortSerializer()

    class Meta:
        model = Post
        fields = ["id", "author", "content", "picture"]


class PostRetrieveSerializer(ModelSerializer):

    author = CustomUserRetrieveSerializer()

    class Meta:
        model = Post
        fields = "__all__"


class PostCommentListSerializer(ModelSerializer):

    author = CharField(source="author.name")

    class Meta:
        model = Post
        fields = ["id", "author", "content", "picture"]
