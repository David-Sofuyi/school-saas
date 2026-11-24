from django.db import models
from django.conf import settings
from apps.core.models import TenantModel

EMPLOYMENT_STATUS_CHOICES = [
    ("active", "Active"),
    ("on_leave", "On Leave"),
    ("suspended", "Suspended"),
    ("terminated", "Terminated"),
    ("resigned", "Resigned"),
]

class TeacherProfile(TenantModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    staff_id = models.CharField(max_length=50, blank=True)
    qualification = models.CharField(max_length=150, blank=True, help_text="e.g. B.Ed, B.Sc, NCE, PGDE")
    specialization = models.CharField(max_length=100, blank=True)
    employment_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default="active")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    resume = models.FileField(upload_to="staff_resumes/", blank=True, null=True)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        unique_together = ("school", "staff_id")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id or 'Staff'})"
