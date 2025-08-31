from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'branch', 'is_active', 'created_date', 'deleted_at']
    list_filter = ['role', 'is_active', 'branch', 'deleted_at']
    search_fields = ['username', 'email', 'branch__name']
    ordering = ['-created_date']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'role', 'branch')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_date', 'updated_date', 'deleted_at')}),
    )
    
    readonly_fields = ['created_date', 'updated_date', 'last_login']
    
    actions = ['soft_delete_users', 'restore_users']
    
    def soft_delete_users(self, request, queryset):
        count = 0
        for user in queryset:
            if not user.deleted_at:
                user.delete()
                count += 1
        self.message_user(request, f'{count} users soft deleted.')
    soft_delete_users.short_description = "Soft delete selected users"
    
    def restore_users(self, request, queryset):
        count = 0
        for user in queryset:
            if user.deleted_at:
                user.restore()
                count += 1
        self.message_user(request, f'{count} users restored.')
    restore_users.short_description = "Restore selected users"