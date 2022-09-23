from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from api.serializers.post import (
    PostCreateOrUpdateSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
)
from api.models.post import Post


def user_is_not_author(user, author):
    return user != author


class PostViewSet(ModelViewSet):

    http_method_names = ["get", "post", "put", "patch", "delete"]
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            return PostCreateOrUpdateSerializer

        elif self.action in ["list"]:
            return PostListSerializer

        elif self.action in ["retrieve"]:
            return PostRetrieveSerializer

        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_data = {
            "author": self.request.user,
            **serializer.validated_data,
        }

        post = Post.objects.create(**post_data)

        return Response(self.get_serializer(post).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can update this post.")

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.partial = False
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
