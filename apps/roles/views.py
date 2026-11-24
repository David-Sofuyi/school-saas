from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.roles.forms import RoleForm, UserRoleAssignForm
from apps.roles.models import Role, UserRole


class CanManageRolesMixin(UserPassesTestMixin):
    """Allows superusers, proprietors, and admins to manage roles."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or getattr(user, "is_platform_superuser", False):
            return True
        return getattr(user, "user_type", None) in ("proprietor", "admin")


class RoleListView(LoginRequiredMixin, CanManageRolesMixin, ListView):
    model = Role
    template_name = "roles/role_list.html"
    context_object_name = "roles"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, "is_platform_superuser", False):
            return Role.objects.all()
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if school:
            return Role.objects.filter(Q(school=school) | Q(school__isnull=True))
        return Role.objects.filter(school__isnull=True)


class RoleCreateView(LoginRequiredMixin, CanManageRolesMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = "roles/role_form.html"
    success_url = reverse_lazy("roles:role-list")

    def form_valid(self, form):
        school = getattr(self.request, "school", None) or getattr(
            self.request.user, "school", None
        )
        form.instance.school = school
        form.instance.is_system_role = False
        return super().form_valid(form)


class UserRoleAssignView(LoginRequiredMixin, CanManageRolesMixin, CreateView):
    model = UserRole
    form_class = UserRoleAssignForm
    template_name = "roles/user_role_assign.html"
    success_url = reverse_lazy("roles:role-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        school = getattr(self.request, "school", None) or getattr(
            self.request.user, "school", None
        )
        kwargs["school"] = school
        return kwargs

    def form_valid(self, form):
        school = getattr(self.request, "school", None) or getattr(
            self.request.user, "school", None
        )
        form.instance.school = school
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)
