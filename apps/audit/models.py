from django.conf import settings
from django.db import models

ACTION_CHOICES = [
    ("create", "Created"),
    ("update", "Updated"),
    ("delete", "Deleted"),
    ("login", "Logged In"),
    ("logout", "Logged Out"),
    ("approve", "Approved"),
    ("reject", "Rejected"),
    ("verify", "Verified"),
    ("publish", "Published"),
    ("upload", "Uploaded"),
    ("download", "Downloaded"),
    ("assign", "Assigned"),
    ("revoke", "Revoked"),
    ("suspend", "Suspended"),
    ("activate", "Activated"),
]


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    object_repr = models.CharField(max_length=255, blank=True)
    previous_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["school", "-timestamp"]),
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["model_name", "object_id"]),
        ]

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} at {self.timestamp}"
