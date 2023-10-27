from django.contrib import admin
from common.admin import GenericModelAdmin

from .models import Todo


class TodoAdmin(GenericModelAdmin):
    list_display = ("title", "description", "user", "completed")
    search_fields = ("title", "description")


admin.site.register(Todo, TodoAdmin)
