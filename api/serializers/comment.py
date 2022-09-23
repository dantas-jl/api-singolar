from rest_framework.serializers import ModelSerializer
from api.models.comment import Comment
from api.serializers.post import PostCommentListSerializer, PostRetrieveSerializer
from users.serializers import CustomUserShortSerializer, CustomUserRetrieveSerializer


class CommentCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content"]
        extra_kwargs = {"author": {"read_only": True}, "post": {"read_only": True}}


class CommentListSerializer(ModelSerializer):

    author = CustomUserShortSerializer()
    post = PostCommentListSerializer()

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content"]


class CommentRetrieveSerializer(ModelSerializer):

    author = CustomUserRetrieveSerializer()
    post = PostRetrieveSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
