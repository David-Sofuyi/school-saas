from django.urls import path
from .views import (
    home_view,
    dashboard_router,
    superuser_dashboard,
    proprietor_dashboard,
    teacher_dashboard,
    parent_dashboard,
    student_dashboard,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("dashboard/", dashboard_router, name="dashboard-router"),
    path("dashboard/superuser/", superuser_dashboard, name="dashboard-superuser"),
    path("dashboard/proprietor/", proprietor_dashboard, name="dashboard-proprietor"),
    path("dashboard/teacher/", teacher_dashboard, name="dashboard-teacher"),
    path("dashboard/parent/", parent_dashboard, name="dashboard-parent"),
    path("dashboard/student/", student_dashboard, name="dashboard-student"),
]
