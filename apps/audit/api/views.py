from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from apps.core.permissions import (
    IsPlatformSuperuser,
    IsSchoolProprietor,
    IsSchoolStaff,
)

from ..models import AuditLog
from ..serializers import AuditLogSerializer


class IsAuditViewer(permissions.BasePermission):
    """Allow platform superusers, proprietors, and school staff to view audit logs."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if getattr(request.user, "is_platform_superuser", False) or request.user.is_superuser:
            return True
        user_type = getattr(request.user, "user_type", None)
        return user_type in {"proprietor", "admin", "principal"}


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing audit logs.
    Read-only for security and integrity.
    """

    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuditViewer]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["action", "model_name", "user", "school"]
    search_fields = ["object_repr", "description", "ip_address", "model_name"]
    ordering_fields = ["timestamp", "action", "model_name"]
    ordering = ["-timestamp"]

    def get_queryset(self):
        user = self.request.user
        qs = AuditLog.objects.select_related("user", "school").all()

        if getattr(user, "is_platform_superuser", False) or user.is_superuser:
            school_id = self.request.query_params.get("school")
            if school_id:
                return qs.filter(school_id=school_id)
            return qs

        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if school:
            return qs.filter(school=school)

        return AuditLog.objects.none()
