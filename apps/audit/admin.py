from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "action",
        "model_name",
        "object_id",
        "object_repr",
        "user",
        "school",
        "ip_address",
    )
    list_filter = ("action", "model_name", "school", "timestamp")
    search_fields = (
        "object_repr",
        "object_id",
        "description",
        "ip_address",
        "user__email",
        "user__username",
    )
    date_hierarchy = "timestamp"
    readonly_fields = [f.name for f in AuditLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent tampering with audit logs; allow superuser only if required
        return request.user.is_superuser
