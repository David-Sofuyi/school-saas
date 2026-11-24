from django.db import models

from apps.core.models import TimeStampedModel


SCHOOL_TYPE_CHOICES = [
    ("primary", "Primary School"),
    ("secondary", "Secondary School"),
    ("both", "Primary and Secondary"),
]

SUBSCRIPTION_STATUS_CHOICES = [
    ("active", "Active"),
    ("trial", "Trial"),
    ("expired", "Expired"),
    ("suspended", "Suspended"),
]

DAYS_OF_WEEK = [
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
]


class School(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="school_logos/", blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)  # Nigerian state
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    website = models.URLField(blank=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES)
    has_primary = models.BooleanField(default=False)
    has_secondary = models.BooleanField(default=False)
    motto = models.CharField(max_length=255, blank=True)
    established_date = models.DateField(null=True, blank=True)

    # Operations
    opening_time = models.TimeField(default="08:00")
    closing_time = models.TimeField(default="16:00")
    resumption_time = models.TimeField(default="07:30")
    working_days = models.JSONField(
        default=list, help_text="List of day numbers: 0=Mon, 4=Fri"
    )

    # Subscription
    subscription_status = models.CharField(
        max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default="trial"
    )
    subscription_plan = models.CharField(max_length=50, blank=True)
    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)
    max_students = models.PositiveIntegerField(default=500)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        # Auto-set has_primary / has_secondary from school_type
        if self.school_type == "primary":
            self.has_primary = True
        elif self.school_type == "secondary":
            self.has_secondary = True
        elif self.school_type == "both":
            self.has_primary = True
            self.has_secondary = True
        super().save(*args, **kwargs)

    @property
    def is_subscription_active(self):
        from django.utils import timezone

        if self.subscription_status in ("active", "trial"):
            if self.subscription_end and self.subscription_end < timezone.now().date():
                return False
            return True
        return False


class SchoolSettings(TimeStampedModel):
    school = models.OneToOneField(
        School, on_delete=models.CASCADE, related_name="settings"
    )
    # Grading
    ca_total = models.PositiveIntegerField(default=40, editable=False)  # Fixed at 40
    exam_total = models.PositiveIntegerField(
        default=60, editable=False
    )  # Fixed at 60
    # Notifications
    enable_sms = models.BooleanField(default=False)
    enable_email = models.BooleanField(default=True)
    attendance_reminder_time = models.TimeField(default="08:30")
    absence_notification_time = models.TimeField(default="09:00")
    # Display
    primary_color = models.CharField(max_length=7, default="#1a73e8")
    secondary_color = models.CharField(max_length=7, default="#34a853")

    class Meta:
        verbose_name_plural = "School settings"

    def __str__(self):
        return f"Settings for {self.school.name}"
