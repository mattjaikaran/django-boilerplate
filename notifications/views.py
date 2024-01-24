from rest_framework import viewsets, mixins, permissions, filters
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.authentication import SessionAuthentication


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Notification.objects.all()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ordering_fields = ["-datetime_created"]

    def get_queryset(self):
        return Notification.objects.all()

    def get_serializer_class(self):
        return NotificationSerializer
