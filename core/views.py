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
    # MagicLinkSerializer,
    # OrganizationSerializer,
    PasswordResetSerializer,
    # TeamSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    ContactSupportSerializer,
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


# Below is WIP
# Trying to implement passwordless login


# generates the token and sends the email to the user
# class EmailLoginView(FormView):
#     template_name = "auth/email_login.html"
#     form_class = EmailLoginForm

#     def get_user(self, email):
#         """Find the user with this email address."""
#         User = get_user_model()
#         try:
#             return User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None

#     def create_link(self, user):
#         """Create a login link for this user."""
#         link = reverse("login")
#         link = self.request.build_absolute_uri(link)
#         link += sesame.utils.get_query_string(user)
#         return link

#     def send_email(self, user, link):
#         """Send an email with this login link to this user."""
#         user.email_user(
#             subject="[django-sesame] Log in to our app",
#             message=f"""\
# Hello,

# You requested that we send you a link to log in to our app:

#     {link}

# Thank you for using django-sesame!
# """,
#         )

#     def email_submitted(self, email):
#         user = self.get_user(email)
#         if user is None:
#             # Ignore the case when no user is registered with this address.
#             # Possible improvement: send an email telling them to register.
#             print("user not found:", email)
#             return
#         link = self.create_link(user)
#         self.send_email(user, link)

#     def form_valid(self, form):
#         self.email_submitted(form.cleaned_data["email"])
#         return render(self.request, "email_login_success.html")


# when a user clicks on the link in the email, this view is called
# it logs the user in
class MagicLinkLogin(views.APIView):
    def post(self, request):
        print(f"self.request.data => {self.request.data}")
        print(f"request.data => {request.data}")
        try:
            print(
                f">>> core/views.py > MagicLinkLogin > request.data: {request.data} <<<"
            )
            # user = CustomUser.objects.filter(email=request.data["email"]).first()
            user = authenticate(request, token=request.data.token)
            print(f"user => {user}")
            sesame_user = sesame.utils.get_user(request.data.token)
            print(f"sesame_user => {sesame_user}")
            login(request, user)
            print(f"login(request, user) => {login(request, user)}")
            return Response(
                {
                    "user": user,
                    "token": request.data["token"],
                    "message": "Magic link sent to your email.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"Error in MagicLinkLogin view => {e}")
            return Response(data={str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class MagicLinkView(views.APIView):
#     def post(self, request):
#         print(f">>> core/views.py > MagicLinkView > request.data: {request.data} <<<")
#         serializer = MagicLinkSerializer(data=request.data)
#         print(f"serializer => {serializer}")
#         print(f"serializer.is_valid() => {serializer.is_valid()}")
#         if serializer.is_valid():
#             # Send the magic link to the user's email
#             # Typically, you'd send an email with a link that includes the 'token' query parameter
#             # Example: https://example.com/login/?token=your-magic-link-token
#             email = serializer.validated_data["email"]
#             # Send the magic link via email
#             print(f">>> core/views.py > MagicLinkView > email: {email} <<<")
#             user = CustomUser.objects.filter(email=email).first()

#             token = sesame.utils.get_token(user)
#             print(f"token => {token}")
#             send_user_login_email(
#                 {
#                     "site_url": utils.get_site_url(),
#                     "email": email,
#                     "token": token,
#                     "login_link": utils.get_site_url() + "/login/?token=" + token,
#                 }
#             )
#             return Response(
#                 {
#                     "email": email,
#                     "token": token,
#                     "message": "Magic link sent to your email.",
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
