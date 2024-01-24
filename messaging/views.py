from rest_framework import viewsets, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
)


class MessageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Message.objects.all()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ordering_fields = ["-datetime_created"]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()


class ConversationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Conversation.objects.all()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    # ordering_fields = ["-datetime_created"]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.all()
