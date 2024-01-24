import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from common.models import AbstractBaseModel
from core.handlers import PrivateMediaStorage


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        normalized_email = self.normalize_email(email).lower()

        # Create user model instance & set password
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # Create user with superuser defaults via **extra_fields
    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self.create_user(email, password, **extra_fields)

    class Meta:
        ordering = ("id",)


def get_organization_upload_path(instance, filename):
    return f"{settings.ENVIRONMENT}/organizations/{instance.id}/{filename}"


# class Organization(AbstractBaseModel):
#     name = models.CharField(max_length=255, unique=False)
#     logo = models.ImageField(
#         max_length=100, upload_to=get_organization_upload_path, blank=True
#     )
#     url = models.URLField(max_length=200, blank=True)
#     owner = models.ForeignKey(
#         "CustomUser",
#         on_delete=models.PROTECT,
#         related_name="org_owner",
#         null=True,
#     )
#     is_developer = models.BooleanField("developer", default=True)
#     is_vendor = models.BooleanField("vendor", default=False)
#     is_consultant = models.BooleanField(
#         "consultant",
#         default=False,
#         help_text="Consultants allowed to do have actions on both sides - buyer/seller",
#     )

#     def __str__(self):
#         return f"Organization: {str(self.name)}"


# class Team(AbstractBaseModel):
#     name = models.CharField(max_length=255)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     members = models.ManyToManyField("CustomUser", related_name="org_teams")

#     def __str__(self):
#         return f"Team: {str(self.name)}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # `password` inherited from `AbstractBaseUser`
    # `is_superuser` inherited from `PermissionsMixin`
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True, error_messages={"unique": "A user with that email already exists"}
    )
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    phone_number_validator = RegexValidator(
        regex=r"^\d{9,15}$", message="Phone number must contain only 9 to 15 digits"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, validators=[phone_number_validator]
    )

    is_admin = models.BooleanField(
        "admin",
        default=False,
        help_text="Gives Users access to the Admin Dashboard",
    )
    is_staff = models.BooleanField(
        "staff",
        default=False,
        help_text="Designates whether the user can log into Django Admin.",
    )
    is_superuser = models.BooleanField(default=False)

    # Users can be members of multiple organizations
    # organizations = models.ManyToManyField(
    #     Organization, related_name="user_orgs", blank=True
    # )

    # Use 'email' for the user's username
    USERNAME_FIELD = "email"

    # Prompt for these required fields when creating a user via `createsuperuser` command
    # 'email' is included automatically since it is set as USERNAME_FIELD
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # @property
    # def token(self):
    #     """
    #     Allows us to get a user's token by calling `user.token` instead of
    #     `user.generate_jwt_token().

    #     The `@property` decorator above makes this possible. `token` is called
    #     a "dynamic property".
    #     """
    #     return self._generate_jwt_token()

    # def _generate_jwt_token(self):
    #     """
    #     Generates a JSON Web Token that stores this user's ID and has an expiry
    #     date set to 60 days into the future.
    #     """
    #     dt = datetime.now() + datetime.timedelta(days=60)

    #     token = jwt.encode(
    #         {"id": self.pk, "exp": int(dt.strftime("%s"))},
    #         settings.SECRET_KEY,
    #         algorithm="HS256",
    #     )

    #     return token.decode("utf-8")

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        ordering = ["email"]
        permissions = (("can_access_settings", "Can access settings"),)
        verbose_name_plural = "Users"


class ContactSupport(AbstractBaseModel):
    email = models.EmailField()
    description = models.TextField(max_length=1500)

    class Meta:
        ordering = ["-datetime_created"]
        verbose_name_plural = "Support Messages"

    # sample model for testing file uploads
    # def get_vertical_path(instance, filename):
    #     return f"{settings.ENVIRONMENT}/products/vertical/{instance.id}/{filename}"

    # image = models.ImageField(max_length=255, upload_to=get_vertical_path, blank=True)
    # icon = models.ImageField(max_length=255, upload_to=get_vertical_path, blank=True)
