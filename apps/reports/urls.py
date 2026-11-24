from django.urls import path
from .views import academic_reports, attendance_reports, financial_reports, calendar_reports

urlpatterns = [
    path("academic/", academic_reports, name="report-academic"),
    path("attendance/", attendance_reports, name="report-attendance"),
    path("financial/", financial_reports, name="report-financial"),
    path("calendar/", calendar_reports, name="report-calendar"),
]
