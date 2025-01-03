from django.contrib import admin
from .models import TestCase


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('execution_result', 'created_at')
