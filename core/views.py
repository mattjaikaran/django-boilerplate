from rest_framework import (
    views,
    viewsets,
    status,
    mixins,
    permissions,
    filters,
    status,
)
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from core.models import CustomUser, ContactSupport
from core.serializers import (
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    ContactSupportSerializer,
    # OrganizationSerializer,
    # TeamSerializer,
)
from core.emails import send_user_login_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    # Permissions are restricted on:
    #   - get_queryset()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


# view for registering users
class RegisterView(views.APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = ()

    def post(self, request):
        try:
            # create user
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.validated_data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(f"Error in RegisterView => {e}")
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return UserRegistrationSerializer


class UserLoginView(TokenObtainPairView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    serializer_class = UserLoginSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Validate user credentials, login, and return serialized user + auth token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(f"serializer.data => {serializer.data}")

        # If the serializer is valid, then the email/password combo is valid.
        # Get the user entity, from which we can get (or create) the auth token
        user = authenticate(**serializer.validated_data)
        if user is None:
            return Response(
                data={
                    "result": "Failed",
                    "message": "Incorrect email and password combination. Please try again.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_data = UserLoginSerializer.login(user, request)
        token = RefreshToken.for_user(user)
        response_data["refresh"] = str(token)
        response_data["access"] = str(token.access_token)
        print(f"response_data UserLoginView => {response_data}")
        return Response(response_data, status=status.HTTP_202_ACCEPTED)


class ForgotPasswordView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.filter(email=email).first()

            if user is not None:
                refresh = RefreshToken.for_user(user)
                # You can send an email with the token for password reset here
                return Response(
                    {
                        "message": "Password reset email sent successfully",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]
            decoded_token = RefreshToken(token)

            try:
                user_id = decoded_token["user_id"]
                user = CustomUser.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password reset successfully"},
                    status=status.HTTP_200_OK,
                )

            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrganizationViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     # Permissions are restricted on:
#     #   - get_queryset()
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = (SessionAuthentication,)


# class TeamViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = (SessionAuthentication,)
#     # Permissions are restricted on:
#     #   - get_queryset()
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print(f">>> core/views.py > LogoutView > request.data: {request.data} <<<")

        try:
            refresh_token = request.data["refresh"]
            print(f"refresh_token => {refresh_token}")
            token = RefreshToken(refresh_token)
            print(f"token => {token}")
            res = token.blacklist()

            return Response(
                data={f"{res} Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(data={str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ContactSupportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ContactSupport.objects.all()
    serializer_class = ContactSupportSerializer
    # Permissions are restricted on:
    #   - get_queryset()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
