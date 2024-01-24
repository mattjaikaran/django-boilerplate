from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions, status
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core import utils
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate
from core.emails import send_support_email, send_user_login_email
from .models import CustomUser, ContactSupport


class UserSerializer(serializers.ModelSerializer):
    # organizations = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Organization.objects.all()
    # )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "is_active",
            # "organizations",
        )
        # exclude = ("password",)


# class OrganizationSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True)
#     # owner = serializers.PrimaryKeyRelatedField(
#     #     queryset=CustomUser.objects.all(), required=True
#     # )

#     class Meta:
#         model = Organization
#         fields = "__all__"

#     def create(self, validated_data):
#         print(f"validated_data => {validated_data}")
#         print(f"self => {self}")
#         organization = Organization.objects.create(
#             name=validated_data["name"],
#             owner=validated_data["owner"],
#         )
#         print(f"organization => {organization}")
#         organization.save()
#         return organization


# class TeamSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True)
#     organization = serializers.PrimaryKeyRelatedField(
#         queryset=Organization.objects.all(), required=True
#     )

#     class Meta:
#         model = Team
#         fields = "__all__"

#     def create(self, validated_data):
#         print(f"validated_data => {validated_data}")
#         print(f"self => {self}")
#         team = Team.objects.create(
#             name=validated_data["name"],
#             organization=validated_data["organization"],
#         )
#         print(f"team => {team}")
#         team.save()
#         return team


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to register users.
    This is an organization level sign up.

    Meaning the user will be the owner of the organization.
    And the organization will have a default team upon signup.
    Users can be added to the team later.
    Users can be added to multiple teams later.
    """

    email = serializers.CharField()
    password = serializers.CharField()
    # organizations = OrganizationSerializer(many=True, required=False)
    # teams = TeamSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data):
        # company_name = self.initial_data.get("company_name")
        try:
            # Create a CustomUser
            user = CustomUser.objects.create(
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
            )
            user.set_password(validated_data["password"])
            # Create an Organization
            # organization = Organization.objects.create(
            #     name=company_name,
            #     owner=user,
            #     is_developer=is_developer,
            #     is_vendor=is_vendor,
            #     is_consultant=is_consultant,
            # )
            # user.organizations.add(organization)
            user.save()

            # Create a Team
            # team_name = organization.name + " Default Team"
            # team = Team.objects.create(
            #     name=team_name,
            #     organization=organization,
            # )
            # Add the user to the team
            # team.members.add(user)
            return user
        except Exception as e:
            return Response(
                data={f"Error in UserRegistrationSerializer - {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password")

    def validate(self, data):
        print(f"data in validate => {data}")
        try:
            user = CustomUser.objects.get(email=data["email"])
            print(f"user in validate UserLoginSerializer => {user}")
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed("User does not exist")
        return data

    def validate_email(self, value):
        """Emails are always stored and compared in lowercase."""
        return value.lower()

    @classmethod
    def get_token(cls, user):
        token = super(UserLoginSerializer, cls).get_token(user)
        print(f"token in get_token => {token}")

        # Add custom claims
        token["email"] = user.email

        return token

    @staticmethod
    def login(user, request):
        """
        Log-in user and append authentication token to serialized response.
        """
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        auth_token, token_created = Token.objects.get_or_create(user=user)
        print(f"auth_token in login => {auth_token}")
        serializer = UserSerializer(user, context={"request": request})
        response_data = serializer.data
        print(f"response_data in login => {response_data}")
        response_data["token"] = auth_token.key
        return response_data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)


# class MagicLinkSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, data):
#         email = data.get("email")
#         user = CustomUser.objects.filter(email=email).first()
#         print(f"email => {email}")
#         print(f"user => {user}")
#         print(f"data => {data}")
#         if user is None:
#             raise exceptions.ValidationError("No user with that email.")
#         return data

#     def create(self, validated_data):
#         try:
#             email = validated_data.get("email")
#             user = CustomUser.objects.filter(email=email).first()
#             print(f"email => {email}")
#             print(f"user => {user}")
#             print(f"validated_data => {validated_data}")
#             token = sesame.utils.get_token(user)
#             print(f"token => {token}")
#             send_user_login_email(
#                 {
#                     "site_url": utils.get_site_url(),
#                     "project_name": validated_data["project"],
#                     "vendor_integrator_name": validated_data["vendor"],
#                 }
#             )
#             return {
#                 "email": email,
#                 "token": token,
#             }
#         except Exception as e:
#             print(f"Exception => {e}")
#             raise exceptions.ValidationError("No user with that email.")


class ContactSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSupport
        fields = "__all__"

    def create(self, validated_data):
        print(f"validated_data", validated_data)
        try:
            email = validated_data["email"]
            description = validated_data["description"]
            print(f"email => {email}")
            print(f"description => {description}")
            contact_support = ContactSupport.objects.create(
                email=email,
                description=description,
            )
            # send email to support team
            context = {
                "user_email": email,
                "message": description,
            }
            send_support_email(context)
            return contact_support
        except Exception as e:
            print(f"Exception create in ContactSupportSerializer => {e}")
            raise exceptions.ValidationError(f"Contact Support failed. => {e}")
