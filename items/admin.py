from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'status', 'reporter', 'created_at', 'uuid']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['name', 'description', 'reporter__email', 'reporter__first_name']
    ordering = ['-created_at']
    list_per_page = 20
    readonly_fields = ['uuid', 'created_at', 'updated_at']

    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'category', 'description', 'photo', 'location_found', 'uuid')
        }),
        ('Status & Ownership', {
            'fields': ('status', 'reporter')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_recovered', 'mark_deactivated']

    def mark_recovered(self, request, queryset):
        queryset.update(status='recovered')
        self.message_user(request, f"{queryset.count()} item(s) marked as recovered.")
    mark_recovered.short_description = "Mark selected items as Recovered"

    def mark_deactivated(self, request, queryset):
        queryset.update(status='deactivated')
        self.message_user(request, f"{queryset.count()} item(s) deactivated.")
    mark_deactivated.short_description = "Deactivate selected items"
