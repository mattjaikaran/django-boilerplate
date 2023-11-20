from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ("username", "first_name", "last_name", "email", "password")
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data["username"],
#             first_name=validated_data["first_name"],
#             last_name=validated_data["last_name"],
#             email=validated_data["email"],
#         )
#         user.set_password(validated_data["password"])
#         user.save()

#         return user
