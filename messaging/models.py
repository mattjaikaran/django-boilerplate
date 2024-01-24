from django.db import models
from django.conf import settings
from common.models import AbstractBaseModel


class Message(AbstractBaseModel):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="messages_sent"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="messages_received",
    )
    content = models.TextField(max_length=512, blank=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message: {str(self.content)} - From {str(self.sender)} to {str(self.recipient)}"


class ConversationQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(participants=user)


class Conversation(AbstractBaseModel):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations"
    )
    messages = models.ManyToManyField(Message, related_name="messages", blank=True)

    objects = ConversationQuerySet.as_manager()

    def participants_list(self):
        return f"Conversation between - " + ", ".join(
            participant.full_name for participant in self.participants.all()
        )

    def __str__(self):
        return f"Conversation: {self.participants_list()}"
