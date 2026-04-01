from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Unregister the default User admin if it exists
try:
    from django.contrib.auth.models import User as DefaultUser
    admin.site.unregister(DefaultUser)
except:
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'phone', 'student_id', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'student_id', 'phone']
    ordering = ['-date_joined']
    list_per_page = 20

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('University Info', {'fields': ('role', 'phone', 'student_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('University Info', {
            'fields': ('role', 'phone', 'student_id')
        }),
    )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email
    get_full_name.short_description = 'Full Name'
