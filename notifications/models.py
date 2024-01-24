from django.db import models
from django.conf import settings
from common.models import AbstractBaseModel
from . import constants


class NotificationQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(recipient=user)


class Notification(AbstractBaseModel):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notifications"
    )
    status = models.CharField(
        max_length=128,
        choices=constants.NOTIFICATION_STATUS_CHOICES,
        default=constants.PENDING,
    )
    type = models.CharField(max_length=128, choices=constants.NOTIFICATION_TYPE_CHOICES)

    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        return f"Notification: {str(self.type)} {str(self.recipient)}"
