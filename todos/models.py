from django.db import models

from core.models import CustomUser


class Todo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=256, blank=True)
    order = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
