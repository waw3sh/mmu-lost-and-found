from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['item', 'claimant', 'status', 'otp_verified', 'handoff_method', 'created_at']
    list_filter = ['status', 'otp_verified', 'created_at']
    search_fields = ['item__name', 'claimant__email', 'claimant__first_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'otp_code']
    list_per_page = 20

    actions = ['mark_collected', 'mark_disputed']

    def mark_collected(self, request, queryset):
        for claim in queryset:
            claim.status = 'COLLECTED'
            claim.save()
            claim.item.status = 'RECOVERED'
            claim.item.save()
        self.message_user(request, f"{queryset.count()} claim(s) marked as collected.")
    mark_collected.short_description = "Mark selected claims as Collected"

    def mark_disputed(self, request, queryset):
        queryset.update(status='DISPUTED')
        self.message_user(request, f"{queryset.count()} claim(s) marked as disputed.")
    mark_disputed.short_description = "Mark selected claims as Disputed"
