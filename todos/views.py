from rest_framework import mixins, viewsets, permissions

from .serializers import TodoSerializer
from .models import Todo


class TodoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Todo.objects.all()
    permission_classes = permissions.IsAuthenticated
    serializer_class = TodoSerializer
