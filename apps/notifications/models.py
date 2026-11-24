from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import TenantModel, TimeStampedModel

NOTIFICATION_TYPE_CHOICES = [
    ("info", "Information"),
    ("success", "Success"),
    ("warning", "Warning"),
    ("error", "Error"),
    ("attendance", "Attendance"),
    ("academic", "Academic"),
    ("financial", "Financial"),
    ("calendar", "Calendar"),
    ("announcement", "Announcement"),
]

CHANNEL_CHOICES = [
    ("in_app", "In-App"),
    ("email", "Email"),
    ("sms", "SMS"),
]


class Notification(TimeStampedModel):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications",
    )
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default="info"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default="in_app")
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    link = models.URLField(blank=True)  # optional link to related page

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read", "-created_at"]),
            models.Index(fields=["school", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} to {self.recipient}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])


class Announcement(TenantModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_announcements",
    )
    target_audience = models.JSONField(
        default=list,
        help_text="List of target user types (e.g. ['student', 'parent', 'teacher']) or ['all']",
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to="announcements/", blank=True, null=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
