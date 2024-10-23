from django.contrib.auth import authenticate

from rest_framework import serializers
from delivery.models import User

from delivery.utils.validation import ValidationError, ValidationCodeEnum

from . import auth


class AuthRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class AuthLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenAuthSerializer(serializers.Serializer):

    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    def run_validation(self, attrs):
        authenticate_kwargs = {
            "username": attrs["username"],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        # noinspection PyAttributeOutsideInit
        user = authenticate(**authenticate_kwargs)

        if user is None:
            raise ValidationError(ValidationCodeEnum.ERR_USER_000)
        if user.is_banned:
            raise ValidationError(ValidationCodeEnum.ERR_USER_001)

        access_token = auth.generate_token(
            username=user.username,
            user_id=user.id,
            role="admin" if user.is_staff else "user",
        )
        refresh_token = auth.generate_refresh_token(user.username)

        data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
        }
        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions", "is_superuser"]
        read_only_fields = [
            "id",
            "is_staff",
            "is_active",
            "is_banned",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
