from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from delivery.models import User
from delivery.services.auth.serializer import (
    AuthLoginSerializer,
    AuthRegisterSerializer,
    TokenAuthSerializer,
    TokenRefreshSerializer,
    UserSerializer,
)

from delivery.utils.decorators import auth_required


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    model = User

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self, user_id=None):
        return User.objects.get(id=user_id)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=["post"], serializer_class=AuthRegisterSerializer)
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()

        response_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        return Response(response_data)

    @action(detail=False, methods=["post"], serializer_class=AuthLoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = TokenAuthSerializer(data=serializer.validated_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=TokenRefreshSerializer,
    )
    def refresh_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return

    @action(
        detail=False,
        methods=["get", "patch"],
        serializer_class=UserSerializer,
        url_path="profile",
    )
    @auth_required(view_type="api-view-set")
    def profile(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = self.get_object(user_id)
        if request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
