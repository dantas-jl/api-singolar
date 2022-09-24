from django.db import IntegrityError
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from api.serializers.like import (
    LikeCreateSerializer,
    LikeListSerializer
)
from api.models.like import Like
from api.utils import user_is_not_author


class LikeViewSet(ModelViewSet):

    http_method_names = ["get", "post", "delete"]
    queryset = Like.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.action in ["create"]:
            return LikeCreateSerializer

        elif self.action in ["list", "retrieve"]:
            return LikeListSerializer
        
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        like_data = {
            "author": self.request.user,
            **serializer.validated_data,
        }

        try:
            like = Like.objects.create(**like_data)
        
        except IntegrityError:
            raise PermissionDenied("You have already liked this comment")

        return Response(
            self.get_serializer(like).data, status=status.HTTP_201_CREATED
        )


    @transaction.atomic
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        if user_is_not_author(self.request.user, instance.author):
            raise PermissionDenied("Only the author can delete this like.")

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
