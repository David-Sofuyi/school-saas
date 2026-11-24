from rest_framework import permissions, viewsets

from apps.schools.models import School, SchoolSettings
from apps.schools.serializers import (
    SchoolListSerializer,
    SchoolSerializer,
    SchoolSettingsSerializer,
)


class IsSuperuser(permissions.BasePermission):
    """Allow access only to superusers."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or getattr(request.user, "is_platform_superuser", False)
            )
        )


class IsProprietorOrSuperuser(permissions.BasePermission):
    """Allow school proprietor or superuser."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser or getattr(
            request.user, "is_platform_superuser", False
        ):
            return True
        return getattr(request.user, "user_type", None) == "proprietor"

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or getattr(
            request.user, "is_platform_superuser", False
        ):
            return True
        school = obj if isinstance(obj, School) else getattr(obj, "school", None)
        user_school = getattr(request, "school", None) or getattr(
            request.user, "school", None
        )
        return (
            school is not None
            and user_school is not None
            and school.pk == user_school.pk
        )


class SchoolViewSet(viewsets.ModelViewSet):
    """
    CRUD for School.
    - list / create: superuser only
    - retrieve / update / partial_update: proprietor (own) or superuser
    - destroy: superuser only
    """

    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get_permissions(self):
        if self.action in ("list", "create", "destroy"):
            return [permissions.IsAuthenticated(), IsSuperuser()]
        return [permissions.IsAuthenticated(), IsProprietorOrSuperuser()]

    def get_serializer_class(self):
        if self.action == "list":
            return SchoolListSerializer
        return SchoolSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or getattr(user, "is_platform_superuser", False)):
            school = getattr(self.request, "school", None) or getattr(
                user, "school", None
            )
            if school:
                qs = qs.filter(pk=school.pk)
            else:
                qs = qs.none()
        return qs


class SchoolSettingsViewSet(viewsets.ModelViewSet):
    """CRUD for SchoolSettings — proprietor or superuser."""

    queryset = SchoolSettings.objects.select_related("school")
    serializer_class = SchoolSettingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsProprietorOrSuperuser]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or getattr(user, "is_platform_superuser", False)):
            school = getattr(self.request, "school", None) or getattr(
                user, "school", None
            )
            if school:
                qs = qs.filter(school=school)
            else:
                qs = qs.none()
        return qs
