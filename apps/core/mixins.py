from django.core.exceptions import PermissionDenied


class TenantQuerySetMixin:
    """
    View / ViewSet mixin that scopes the queryset to the current tenant.

    Expects ``request.school`` to be set by ``TenantMiddleware``.

    * If the user is a platform superuser and no school context is set the
      full (unfiltered) queryset is returned — this lets platform-level
      dashboards work.
    * Otherwise, if ``request.school`` is ``None`` a ``PermissionDenied`` is
      raised so that no data leaks across tenants.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        school = getattr(self.request, "school", None)

        if school is not None:
            return qs.filter(school=school)

        # No school context.
        if getattr(self.request.user, "is_platform_superuser", False):
            return qs

        raise PermissionDenied(
            "No school context available. "
            "You must be associated with a school to access this resource."
        )


class TenantCreateMixin:
    """
    View / ViewSet mixin that stamps the tenant on newly created objects.

    Works with both DRF (``perform_create(serializer)``) and plain Django
    class-based views (``form_valid(form)``).
    """

    def perform_create(self, serializer):
        serializer.save(school=self.request.school)
