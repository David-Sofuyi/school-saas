from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from apps.roles.models import Role, UserRole
from apps.roles.serializers import RoleSerializer, UserRoleSerializer


class IsRoleManagerOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods to authenticated users.
    Allow mutations to superusers, proprietors, and school admins.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or getattr(
            request.user, "is_platform_superuser", False
        ):
            return True
        return getattr(request.user, "user_type", None) in ("proprietor", "admin")


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Role listing and management.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsRoleManagerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, "is_platform_superuser", False):
            return Role.objects.all()
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if school:
            from django.db.models import Q

            return Role.objects.filter(Q(school=school) | Q(school__isnull=True))
        return Role.objects.filter(school__isnull=True)

    def perform_create(self, serializer):
        user = self.request.user
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if not school and not (
            user.is_superuser or getattr(user, "is_platform_superuser", False)
        ):
            raise PermissionDenied("A school context is required to create a role.")
        serializer.save(school=school, is_system_role=False)


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for assigning and managing UserRoles.
    """

    queryset = UserRole.objects.select_related("user", "role", "school", "assigned_by")
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsRoleManagerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, "is_platform_superuser", False):
            return self.queryset
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if school:
            if getattr(user, "user_type", None) in ("proprietor", "admin"):
                return self.queryset.filter(school=school)
            return self.queryset.filter(school=school, user=user)
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if not school:
            raise PermissionDenied("A school context is required to assign user roles.")
        serializer.save(school=school, assigned_by=user)
