"""
URL configuration for school_saas project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.accounts.views import LoginView, LogoutView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Direct Auth Shortcuts
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # API v1 Endpoints
    path("api/v1/core/", include("apps.core.api.urls")),
    path("api/v1/accounts/", include("apps.accounts.api.urls")),
    path("api/v1/schools/", include("apps.schools.api.urls")),
    path("api/v1/roles/", include("apps.roles.api.urls")),
    path("api/v1/classes/", include("apps.classes.api.urls")),
    path("api/v1/teachers/", include("apps.teachers.api.urls")),
    path("api/v1/students/", include("apps.students.api.urls")),
    path("api/v1/parents/", include("apps.parents.api.urls")),
    path("api/v1/academics/", include("apps.academics.api.urls")),
    path("api/v1/attendance/", include("apps.attendance.api.urls")),
    path("api/v1/calendar/", include("apps.calendar_app.api.urls")),
    path("api/v1/fees/", include("apps.fees.api.urls")),
    path("api/v1/payments/", include("apps.payments.api.urls")),
    path("api/v1/timetables/", include("apps.timetables.api.urls")),
    path("api/v1/subscriptions/", include("apps.subscriptions.api.urls")),
    path("api/v1/audit/", include("apps.audit.api.urls")),
    path("api/v1/notifications/", include("apps.notifications.api.urls")),

    # Web Portals & Dashboards
    path("", include("apps.dashboards.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("schools/", include("apps.schools.urls")),
    path("classes/", include("apps.classes.urls")),
    path("teachers/", include("apps.teachers.urls")),
    path("students/", include("apps.students.urls")),
    path("parents/", include("apps.parents.urls")),
    path("academics/", include("apps.academics.urls")),
    path("attendance/", include("apps.attendance.urls")),
    path("calendar/", include("apps.calendar_app.urls")),
    path("fees/", include("apps.fees.urls")),
    path("payments/", include("apps.payments.urls")),
    path("timetables/", include("apps.timetables.urls")),
    path("subscriptions/", include("apps.subscriptions.urls")),
    path("reports/", include("apps.reports.urls")),
    path("audit/", include("apps.audit.urls")),
    path("notifications/", include("apps.notifications.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    try:
        import debug_toolbar  # noqa: F401
        urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
    except ImportError:
        pass
