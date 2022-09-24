from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from api.serializers.comment import (
    CommentCreateOrUpdateSerializer,
    CommentListSerializer,
    CommentRetrieveSerializer,
)
from api.serializers.like import LikeListSerializer
from api.models.comment import Comment
from api.utils import user_is_not_author


class CommentViewSet(ModelViewSet):

    http_method_names = ["get", "post", "put", "patch", "delete"]
    queryset = Comment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            return CommentCreateOrUpdateSerializer

        elif self.action in ["list"]:
            return CommentListSerializer

        elif self.action in ["retrieve"]:
            return CommentRetrieveSerializer

        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_data = {
            "author": self.request.user,
            **serializer.validated_data,
        }

        comment = Comment.objects.create(**comment_data)

        return Response(
            self.get_serializer(comment).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can update this comment.")

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.partial = False
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can partial update this comment.")

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.partial = True
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can delete this comment.")

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=True, methods=["get"], url_path="likes(?:/(?P<like_pk>[^/.]+))?")
    def likes(self, request, pk=None, like_pk=None):

        instance = self.get_object()

        if like_pk is None:
            likes = instance.likes.all()
            return Response(
                LikeListSerializer(likes, many=True).data,
                status=status.HTTP_200_OK,
            )

        else:
            like = get_object_or_404(instance.likes, pk=like_pk)
            return Response(LikeListSerializer(like).data, status=status.HTTP_200_OK)
