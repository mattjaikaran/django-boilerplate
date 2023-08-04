from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email")


admin.site.register(CustomUser, CustomUserAdmin)