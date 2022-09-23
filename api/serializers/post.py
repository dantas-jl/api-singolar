from rest_framework.serializers import ModelSerializer
from api.models.post import Post

class PostCreateOrUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = Post
        fields = ["id", "author", "content", "picture"]
        extra_kwargs = {"author": {"read_only": True}}
        