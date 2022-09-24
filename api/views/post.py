from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from api.serializers.post import (
    PostCreateOrUpdateSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
)
from api.serializers.comment import CommentListSerializer, CommentRetrieveSerializer
from api.models.post import Post
from api.utils import user_is_not_author


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

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can partial update this post.")

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.partial = True
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can delete this post.")

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(
        detail=True, methods=["get"], url_path="comments(?:/(?P<comment_pk>[^/.]+))?"
    )
    def comments(self, request, pk=None, comment_pk=None):

        instance = self.get_object()

        if comment_pk is None:
            comments = instance.comments.all()
            return Response(
                CommentListSerializer(comments, many=True).data,
                status=status.HTTP_200_OK,
            )

        else:
            comment = get_object_or_404(instance.comments, pk=comment_pk)
            return Response(
                CommentRetrieveSerializer(comment).data, status=status.HTTP_200_OK
            )
