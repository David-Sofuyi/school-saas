from django.conf import settings
from django.db import models

from apps.core.models import TenantModel, TimeStampedModel

PERMISSION_CHOICES = [
    ("manage_school", "Manage School Settings"),
    ("manage_users", "Manage Users"),
    ("manage_students", "Manage Students"),
    ("manage_teachers", "Manage Teachers"),
    ("manage_parents", "Manage Parents"),
    ("manage_classes", "Manage Classes"),
    ("manage_subjects", "Manage Subjects"),
    ("manage_fees", "Manage Fees"),
    ("manage_payments", "Manage Payments"),
    ("manage_attendance", "Manage Attendance"),
    ("manage_academics", "Manage Academics"),
    ("manage_calendar", "Manage Calendar"),
    ("manage_events", "Manage Events"),
    ("approve_results", "Approve Results"),
    ("verify_attendance", "Verify Teacher Attendance"),
    ("view_reports", "View Reports"),
    ("view_financials", "View Financial Reports"),
    ("manage_timetable", "Manage Timetable"),
    ("send_notifications", "Send Notifications"),
]


class Role(TimeStampedModel):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roles",
    )
    description = models.TextField(blank=True)
    is_system_role = models.BooleanField(default=False)  # True for default roles
    permissions = models.JSONField(default=list)  # List of permission codenames

    class Meta:
        unique_together = ("name", "school")
        ordering = ["name"]

    def __str__(self):
        if self.school:
            return f"{self.name} ({self.school.name})"
        return f"{self.name} (Global)"


class UserRole(TenantModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_roles",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "role", "school")
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.user} - {self.role.name} ({self.school.name})"
