from rest_framework.serializers import ModelSerializer, CharField
from api.models.comment import Comment
from api.serializers.post import PostCommentListSerializer, PostRetrieveSerializer
from users.serializers import CustomUserShortSerializer, CustomUserRetrieveSerializer


class CommentCreateOrUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content"]
        extra_kwargs = {"author": {"read_only": True}}


class CommentListSerializer(ModelSerializer):

    author = CustomUserShortSerializer()
    post = PostCommentListSerializer()    

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content"]

    
    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response["likes"] = instance.likes.count()

        return response

class CommentRetrieveSerializer(ModelSerializer):

    author = CustomUserRetrieveSerializer()
    post = PostRetrieveSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
    
    def to_representation(self, instance):
        
        response = super().to_representation(instance)
        response["likes"] = instance.likes.count()

        return response

class CommentLikeSerializer(ModelSerializer):

    author = CharField(source="author.name")
    post = PostCommentListSerializer()

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content"]