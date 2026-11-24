"""
DRF permission classes for the Nigerian School Management SaaS.

All classes follow the convention of checking ``request.user`` attributes
(``is_platform_superuser``, ``user_type``, ``school``) set on the
``CustomUser`` model.
"""

from rest_framework.permissions import BasePermission

# ---------------------------------------------------------------------------
# Role-based permissions
# ---------------------------------------------------------------------------


class IsPlatformSuperuser(BasePermission):
    """Allow only platform-level superusers."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_platform_superuser", False)
        )


class IsSchoolProprietor(BasePermission):
    """Allow only users whose ``user_type`` is *proprietor*."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "proprietor"
        )


class IsSchoolStaff(BasePermission):
    """
    Allow any school staff member.

    Staff roles: proprietor, admin, principal, teacher, bursar.
    """

    STAFF_TYPES = {"proprietor", "admin", "principal", "teacher", "bursar"}

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) in self.STAFF_TYPES
        )


class IsTeacher(BasePermission):
    """Allow only teachers."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "teacher"
        )


class IsPrincipal(BasePermission):
    """Allow only principals / head teachers."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "principal"
        )


class IsBursar(BasePermission):
    """Allow only bursars / accountants."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "bursar"
        )


class IsParent(BasePermission):
    """Allow only parents / guardians."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "parent"
        )


class IsStudent(BasePermission):
    """Allow only students."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "student"
        )


# ---------------------------------------------------------------------------
# Object-level permissions
# ---------------------------------------------------------------------------


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission: allow writes only if ``request.user`` is the
    object owner.  Read-only methods (GET, HEAD, OPTIONS) are always allowed
    for authenticated users.

    The owner field is determined by checking, in order: ``user``, ``owner``,
    ``created_by`` on the object.
    """

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS:
            return True

        owner = (
            getattr(obj, "user", None)
            or getattr(obj, "owner", None)
            or getattr(obj, "created_by", None)
        )
        return owner == request.user


class HasSchoolAccess(BasePermission):
    """
    Object-level permission that ensures the requesting user belongs to the
    same school as the object.

    Platform superusers bypass the check.
    """

    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "is_platform_superuser", False):
            return True

        obj_school = getattr(obj, "school", None)
        user_school = getattr(request.user, "school", None)

        if obj_school is None or user_school is None:
            return False

        return obj_school.pk == user_school.pk
