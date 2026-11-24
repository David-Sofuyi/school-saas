from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    """
    Attach ``request.school`` for every request.

    Rules:
    * Skip Django admin URLs entirely (``/admin/``).
    * Superusers may switch tenant context via the ``X-School-ID`` header or
      a ``school_id`` query-string parameter.
    * Authenticated users with a ``school`` FK get that school attached.
    * Everyone else gets ``request.school = None``.
    """

    def process_request(self, request):
        # Always initialise the attribute so downstream code can rely on it.
        request.school = None

        # Don't interfere with the Django admin.
        if request.path.startswith("/admin/"):
            return None

        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return None

        if user.is_platform_superuser:
            # Allow superusers to impersonate a school via header / query param.
            school_id = (
                request.META.get("HTTP_X_SCHOOL_ID")
                or request.GET.get("school_id")
            )
            if school_id:
                # Lazy import to avoid circular dependencies at module level.
                from apps.schools.models import School

                try:
                    request.school = School.objects.get(pk=school_id)
                except School.DoesNotExist:
                    request.school = None
            else:
                # Superuser without an explicit context — leave as None.
                request.school = None
        else:
            # Regular authenticated user: use their own school.
            request.school = getattr(user, "school", None)

        return None
