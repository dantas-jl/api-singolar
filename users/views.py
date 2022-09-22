from re import S
from django.db import transaction
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import (
    CustomUserCreateOrUpdateSerializer,
    CustomUserListSerializer,
    CustomUserRetrieveSerializer,
)


class CustomUserViewSet(ModelViewSet):

    http_method_names = ["get", "post", "put", "patch", "delete"]
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            return CustomUserCreateOrUpdateSerializer

        elif self.action in ["list"]:
            return CustomUserListSerializer

        elif self.action in ["retrieve"]:
            return CustomUserRetrieveSerializer

        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        custom_user = CustomUser.objects.create_user(**validated_data)
        return Response(
            self.get_serializer(instance=custom_user).data,
            status=status.HTTP_201_CREATED,
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.partial = False
        custom_user = serializer.save()

        password = serializer.validated_data["password"]
        custom_user.set_password(password)
        custom_user.save()

        return Response(
            self.get_serializer(instance=custom_user).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        custom_user = serializer.save()

        if serializer.validated_data.get("password"):
            password = serializer.validated_data["password"]
            custom_user.set_password(password)
            custom_user.save()

        return Response(
            self.get_serializer(instance=custom_user).data, status=status.HTTP_200_OK
        )

    def list(self, request, *args, **kwargs):

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
