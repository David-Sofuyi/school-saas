from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.utils.dateparse import parse_date
from django.views.generic import DetailView, ListView

from .models import ACTION_CHOICES, AuditLog


class AuditLogPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensure user is platform superuser, proprietor, or school administrator."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "is_platform_superuser", False) or user.is_superuser:
            return True
        return getattr(user, "user_type", None) in {"proprietor", "admin", "principal"}


class AuditLogListView(AuditLogPermissionMixin, ListView):
    """Web view to list and filter audit log records."""

    model = AuditLog
    template_name = "audit/auditlog_list.html"
    context_object_name = "audit_logs"
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        qs = AuditLog.objects.select_related("user", "school").all()

        # Multi-tenant scoping
        if not (getattr(user, "is_platform_superuser", False) or user.is_superuser):
            school = getattr(self.request, "school", None) or getattr(user, "school", None)
            if school:
                qs = qs.filter(school=school)
            else:
                return AuditLog.objects.none()
        else:
            school_filter = self.request.GET.get("school")
            if school_filter:
                qs = qs.filter(school_id=school_filter)

        # Filters
        action = self.request.GET.get("action")
        if action:
            qs = qs.filter(action=action)

        model_name = self.request.GET.get("model_name")
        if model_name:
            qs = qs.filter(model_name__icontains=model_name)

        user_query = self.request.GET.get("user")
        if user_query:
            if user_query.isdigit():
                qs = qs.filter(user_id=user_query)
            else:
                qs = qs.filter(user__email__icontains=user_query)

        date_from = self.request.GET.get("date_from")
        if date_from:
            parsed_date_from = parse_date(date_from)
            if parsed_date_from:
                qs = qs.filter(timestamp__date__gte=parsed_date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            parsed_date_to = parse_date(date_to)
            if parsed_date_to:
                qs = qs.filter(timestamp__date__lte=parsed_date_to)

        search_q = self.request.GET.get("q")
        if search_q:
            qs = qs.filter(
                models.Q(object_repr__icontains=search_q)
                | models.Q(description__icontains=search_q)
                | models.Q(ip_address__icontains=search_q)
            )

        return qs.order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_choices"] = ACTION_CHOICES
        context["filter_action"] = self.request.GET.get("action", "")
        context["filter_model"] = self.request.GET.get("model_name", "")
        context["filter_user"] = self.request.GET.get("user", "")
        context["filter_date_from"] = self.request.GET.get("date_from", "")
        context["filter_date_to"] = self.request.GET.get("date_to", "")
        context["filter_q"] = self.request.GET.get("q", "")
        return context


class AuditLogDetailView(AuditLogPermissionMixin, DetailView):
    """Web view to inspect detailed changes for an audit log record."""

    model = AuditLog
    template_name = "audit/auditlog_detail.html"
    context_object_name = "log"

    def get_queryset(self):
        user = self.request.user
        qs = AuditLog.objects.select_related("user", "school").all()
        if not (getattr(user, "is_platform_superuser", False) or user.is_superuser):
            school = getattr(self.request, "school", None) or getattr(user, "school", None)
            if school:
                qs = qs.filter(school=school)
            else:
                return AuditLog.objects.none()
        return qs
