from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.schools.forms import SchoolRegistrationForm, SchoolSettingsForm
from apps.schools.models import School, SchoolSettings


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Only allow superusers or platform superusers."""

    def test_func(self):
        user = self.request.user
        return bool(
            user.is_authenticated
            and (user.is_superuser or getattr(user, "is_platform_superuser", False))
        )


class ProprietorOrSuperuserMixin(UserPassesTestMixin):
    """Allow the school's proprietor or a superuser."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or getattr(user, "is_platform_superuser", False):
            return True
        return getattr(user, "user_type", None) == "proprietor"


# ---------------------------------------------------------------------------
# School CRUD
# ---------------------------------------------------------------------------


class SchoolListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """Superuser-only: list every school on the platform."""

    model = School
    template_name = "schools/school_list.html"
    context_object_name = "schools"
    paginate_by = 20


class SchoolDetailView(LoginRequiredMixin, ProprietorOrSuperuserMixin, DetailView):
    """Proprietor sees their own school; superuser can see any."""

    model = School
    template_name = "schools/school_detail.html"
    context_object_name = "school"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or getattr(user, "is_platform_superuser", False)):
            school = getattr(self.request, "school", None) or getattr(user, "school", None)
            if school:
                qs = qs.filter(pk=school.pk)
            else:
                qs = qs.none()
        return qs


class SchoolCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    """Superuser creates a new school."""

    model = School
    form_class = SchoolRegistrationForm
    template_name = "schools/school_form.html"
    success_url = reverse_lazy("schools:school-list")


class SchoolUpdateView(LoginRequiredMixin, ProprietorOrSuperuserMixin, UpdateView):
    """Proprietor or superuser updates school details."""

    model = School
    form_class = SchoolRegistrationForm
    template_name = "schools/school_form.html"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or getattr(user, "is_platform_superuser", False)):
            school = getattr(self.request, "school", None) or getattr(user, "school", None)
            if school:
                qs = qs.filter(pk=school.pk)
            else:
                qs = qs.none()
        return qs

    def get_success_url(self):
        return reverse_lazy("schools:school-detail", kwargs={"pk": self.object.pk})


# ---------------------------------------------------------------------------
# School Settings
# ---------------------------------------------------------------------------


class SchoolSettingsView(LoginRequiredMixin, ProprietorOrSuperuserMixin, UpdateView):
    """Proprietor manages school settings."""

    model = SchoolSettings
    form_class = SchoolSettingsForm
    template_name = "schools/school_settings.html"

    def get_object(self, queryset=None):
        school = get_object_or_404(School, pk=self.kwargs["pk"])
        obj, _created = SchoolSettings.objects.get_or_create(school=school)
        return obj

    def get_success_url(self):
        return reverse_lazy("schools:school-settings", kwargs={"pk": self.kwargs["pk"]})
