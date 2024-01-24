from django.contrib import admin
from common.admin import GenericModelAdmin
from .models import Conversation, Message


class ConversationAdmin(GenericModelAdmin):
    list_display = (
        "id",
        "participants_list",
        "datetime_created",
    )
    filter_horizontal = (
        "participants",
    )  # Allow  selecting participants in a user-friendly way
    readonly_fields = ("id",)
    ordering = ("-datetime_created",)


class MessageAdmin(GenericModelAdmin):
    list_display = ("content", "sender", "recipient", "id", "datetime_created")
    list_filter = ("sender", "datetime_created")
    search_fields = ("sender__email", "content__str")
    readonly_fields = ("id",)
    ordering = ("-datetime_created",)


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
