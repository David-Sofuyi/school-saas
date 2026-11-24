from django.contrib import admin

from apps.roles.models import Role, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "is_system_role", "created_at")
    list_filter = ("is_system_role", "school")
    search_fields = ("name", "description")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "school", "assigned_by", "assigned_at")
    list_filter = ("role", "school")
    search_fields = ("user__email", "user__username", "role__name")
    list_select_related = ("user", "role", "school", "assigned_by")
