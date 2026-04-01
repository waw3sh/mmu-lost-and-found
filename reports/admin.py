from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['item', 'location_found', 'finder_name', 'finder_email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['item__name', 'location_found', 'finder_name', 'finder_email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    list_per_page = 20
