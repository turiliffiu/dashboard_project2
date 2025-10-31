from django.contrib import admin
from .models import ProcedureCategory

# Register your models here.

@admin.register(ProcedureCategory)
class ProcedureCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'filename', 'order']
    list_editable = ['order']
    search_fields = ['name', 'description']