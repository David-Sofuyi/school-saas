from django.db import models
from django.conf import settings
from apps.core.models import TenantModel, TimeStampedModel
from apps.academics.models import AcademicSession, AcademicTerm

class PublicHoliday(TimeStampedModel):
    title = models.CharField(max_length=150, help_text="e.g. Independence Day, Eid al-Fitr, Democracy Day")
    date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, blank=True)
    is_provisional = models.BooleanField(default=False, help_text="Provisional until official federal announcement")
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_holidays")

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.title} ({self.date})"


class SchoolHoliday(TenantModel):
    HOLIDAY_TYPE_CHOICES = [
        ("mid_term", "Mid-Term Break"),
        ("end_term_1", "End of First Term"),
        ("end_term_2", "End of Second Term"),
        ("end_term_3", "End of Third Term"),
        ("christmas", "Christmas Vacation"),
        ("easter", "Easter Vacation"),
        ("long_vacation", "Long Vacation (Summer)"),
        ("special_closure", "Special School Closure"),
        ("emergency", "Emergency Closure"),
        ("other", "Other School Holiday"),
    ]
    name = models.CharField(max_length=150)
    holiday_type = models.CharField(max_length=30, choices=HOLIDAY_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="holidays")
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True, related_name="holidays")
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class AcademicEvent(TenantModel):
    CATEGORY_CHOICES = [
        ("academic", "Academic (Exam, Resumption, Revision)"),
        ("meeting", "Meeting (PTA, Staff, Board)"),
        ("sports", "Sports & Competitions"),
        ("cultural", "Cultural & Social"),
        ("educational", "Educational (Excursions, Science Fair)"),
        ("administrative", "Administrative (Admissions, Inspections)"),
        ("custom", "Custom School Category"),
    ]
    AUDIENCE_CHOICES = [
        ("whole_school", "Entire School"),
        ("primary", "Primary Section Only"),
        ("secondary", "Secondary Section Only"),
        ("teachers", "Teachers & Staff"),
        ("parents", "Parents Only"),
        ("students", "Students Only"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="academic")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="events")
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=150, blank=True)
    target_audience = models.CharField(max_length=30, choices=AUDIENCE_CHOICES, default="whole_school")
    reminder_enabled = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published")
    attachment = models.FileField(upload_to="event_circulars/", blank=True, null=True)

    class Meta:
        ordering = ["start_date", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.start_date})"


class SchoolAcademicCalendarDocument(TenantModel):
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="calendar_documents")
    term = models.ForeignKey(AcademicTerm, on_delete=models.SET_NULL, null=True, blank=True, related_name="calendar_documents")
    title = models.CharField(max_length=200, help_text="e.g. Approved 2026/2027 Calendar of Activities")
    description = models.TextField(blank=True)
    current_file = models.FileField(upload_to="academic_calendars/")
    file_format = models.CharField(max_length=10, help_text="pdf, docx, xlsx, jpg, png")
    current_version_number = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)
    visible_to_parents = models.BooleanField(default=True)
    visible_to_students = models.BooleanField(default=True)
    visible_to_teachers = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} (v{self.current_version_number})"


class CalendarDocumentVersion(TenantModel):
    document = models.ForeignKey(SchoolAcademicCalendarDocument, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to="academic_calendars/versions/")
    change_summary = models.TextField(help_text="Notes on what changed in this calendar edition")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number"]
        unique_together = ("document", "version_number")

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
