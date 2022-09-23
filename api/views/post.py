from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from api.serializers.post import PostCreateOrUpdateSerializer
from api.models.post import Post
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class PostViewSet(ModelViewSet):

    http_method_names = ["get", "post", "put", "patch", "delete"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        
        if self.action in ["create", "update", "partial_update"]:
            return PostCreateOrUpdateSerializer

        return super().get_serializer_class()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_data = {
            'author': self.request.user,
            **serializer.validated_data,
        }

        post = Post.objects.create(**post_data)

        return Response(self.get_serializer(post).data, status=status.HTTP_201_CREATED)
    

