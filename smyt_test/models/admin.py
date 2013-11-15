from django.contrib import admin
from .models import Model, Field


class FieldInline(admin.StackedInline):
    model = Field


class ModelAdmin(admin.ModelAdmin):
    inlines = [FieldInline]


admin.site.register(Model, ModelAdmin)
