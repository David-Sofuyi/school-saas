from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from apps.roles.utils import has_permission


def permission_required(permission_codename):
    """
    Decorator for views that checks whether the user has a specific permission
    (via their assigned roles, or platform superuser / proprietor status).
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            school = getattr(request, "school", None) or getattr(
                request.user, "school", None
            )
            if not has_permission(request.user, permission_codename, school=school):
                raise PermissionDenied(
                    "You do not have permission to perform this action."
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def school_role_required(*user_types):
    """
    Decorator for views that checks whether user.user_type is in the allowed types.
    Superusers and platform superusers always pass.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or getattr(
                request.user, "is_platform_superuser", False
            ):
                return view_func(request, *args, **kwargs)
            current_type = getattr(request.user, "user_type", None)
            if current_type not in user_types:
                raise PermissionDenied(
                    "Your user role is not authorized to access this page."
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
