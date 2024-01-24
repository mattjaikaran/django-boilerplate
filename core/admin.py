from django.contrib import admin

from common.admin import GenericModelAdmin
from .models import CustomUser, ContactSupport


class CustomUserAdmin(GenericModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    exclude = ("password",)


# class TeamAdmin(GenericModelAdmin):
#     list_display = ("name", "organization")
#     search_fields = ("name", "organization")


# class OrganizationAdmin(GenericModelAdmin):
#     list_display = ("name", "owner",)
#     search_fields = ("name", "owner")


class ContactSupportAdmin(GenericModelAdmin):
    list_display = ("email", "description")
    search_fields = ("email", "description")


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(Team, TeamAdmin)
admin.site.register(ContactSupport, ContactSupportAdmin)
