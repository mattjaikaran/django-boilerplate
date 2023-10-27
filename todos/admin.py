from django.contrib import admin
from common.admin import GenericModelAdmin
from unfold.admin import ModelAdmin

from .models import Todo


class TodoAdmin(GenericModelAdmin, ModelAdmin):
    list_display = ("title", "description", "user", "completed")
    search_fields = ("title", "description")


admin.site.register(Todo, TodoAdmin)
