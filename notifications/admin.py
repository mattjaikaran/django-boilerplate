from django.contrib import admin
from common.admin import GenericModelAdmin
from .models import Notification


class NotificationAdmin(GenericModelAdmin):
    list_display = ("id", "recipient", "status", "type", "datetime_created")
    ordering = ("-datetime_created",)


admin.site.register(Notification, NotificationAdmin)
