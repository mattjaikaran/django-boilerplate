from rest_framework import mixins, viewsets, views, permissions, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = permissions.IsAuthenticated
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    def post(self, request):
        print(f"request.data => {request.data}")
        serializer = UserSerializer(data=request.data)
        print(f"serializer.data => {serializer.data}")
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        return UserSerializer


class LogoutView(generics.CreateAPIView):
    # permission_classes = (permissions.IsAuthenticated)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # this token cannot authenticate a user again

            return Response(
                data="Logged out successfully", status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                data={f"error in LogoutView {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_serializer_class(self):
        return UserSerializer
