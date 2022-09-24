from rest_framework.serializers import ModelSerializer
from api.models.like import Like
from api.serializers.comment import CommentLikeSerializer
from users.serializers import CustomUserShortSerializer

class LikeCreateSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "author", "comment"]
        extra_kwargs = {"author": {"read_only": True}}


class LikeListSerializer(ModelSerializer):
    
    author = CustomUserShortSerializer()
    comment = CommentLikeSerializer()

    class Meta:
        model = Like
        fields = ["id", "author", "comment"]