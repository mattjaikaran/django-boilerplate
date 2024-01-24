from django.contrib import admin
from django.db import models
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin


class GenericModelAdmin(ImportExportModelAdmin, ModelAdmin, admin.ModelAdmin):
    """
    Generic Model Admin with default fields for search and filter options.
    Search filter for name field
    Filter boxes for all boolean and choice fields in a Model
    """

    def get_search_fields(self, request):
        return self.get_name_field_if_exists()

    def get_ordering(self, request):
        return self.get_name_field_if_exists()

    def get_name_field_if_exists(self):
        if "name" in [field.name for field in self.model._meta.get_fields()]:
            return ["name"]
        else:
            return []

    def get_list_filter(self, request):
        return [
            field.name
            for field in self.model._meta.get_fields()
            if type(field) is models.BooleanField
            or (type(field) is models.CharField and field.choices is not None)
        ]

    def has_delete_permission(self, request, obj=None) -> bool:
        return not request.user.is_staff or request.user.is_superuser
