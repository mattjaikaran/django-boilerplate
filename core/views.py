from rest_framework import mixins, viewsets, permissions

from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = CustomUserSerializer