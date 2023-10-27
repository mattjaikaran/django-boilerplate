from django.contrib import admin

from common.admin import GenericModelAdmin
from .models import CustomUser


class CustomUserAdmin(GenericModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")


admin.site.register(CustomUser, CustomUserAdmin)
