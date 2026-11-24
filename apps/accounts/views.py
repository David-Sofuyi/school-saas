from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# ---------------------------------------------------------------------------
# Authentication views
# ---------------------------------------------------------------------------


class LoginView(auth_views.LoginView):
    """Login view that uses email-based authentication."""

    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    """Logout and redirect to the login page."""

    next_page = "accounts:login"


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display the current user's profile."""

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


# ---------------------------------------------------------------------------
# Dashboard redirect
# ---------------------------------------------------------------------------

# Maps user_type → named URL for the appropriate dashboard.
_DASHBOARD_ROUTES = {
    "superuser": "accounts:profile",  # placeholder until admin dashboard exists
    "proprietor": "accounts:profile",
    "admin": "accounts:profile",
    "principal": "accounts:profile",
    "teacher": "accounts:profile",
    "bursar": "accounts:profile",
    "parent": "accounts:profile",
    "student": "accounts:profile",
}


class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    """
    Redirect the user to the appropriate dashboard based on ``user_type``.

    Falls back to the profile page when no specific dashboard route is
    configured.
    """

    template_name = "accounts/profile.html"  # fallback

    def get(self, request, *args, **kwargs):
        route = _DASHBOARD_ROUTES.get(
            getattr(request.user, "user_type", ""), "accounts:profile"
        )
        return redirect(route)
