from django.db import models
from django.conf import settings
from apps.core.models import TenantModel
from apps.classes.models import ClassArm

GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]

STUDENT_STATUS_CHOICES = [
    ("active", "Active"),
    ("promoted", "Promoted"),
    ("transferred", "Transferred"),
    ("withdrawn", "Withdrawn"),
    ("graduated", "Graduated"),
    ("suspended", "Suspended"),
]

class Student(TenantModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_profile")
    admission_number = models.CharField(max_length=50, unique=True, help_text="Unique Student ID (e.g. STU-2026-001)")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    photograph = models.ImageField(upload_to="student_photos/", blank=True, null=True)
    admission_date = models.DateField()
    current_class_arm = models.ForeignKey(ClassArm, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    status = models.CharField(max_length=20, choices=STUDENT_STATUS_CHOICES, default="active")
    blood_group = models.CharField(max_length=5, blank=True)
    medical_notes = models.TextField(blank=True)
    home_address = models.TextField(blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["school", "admission_number"]),
            models.Index(fields=["school", "status"]),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.admission_number})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudentDocument(TenantModel):
    DOC_TYPES = [
        ("birth_cert", "Birth Certificate"),
        ("previous_result", "Previous Academic Result"),
        ("medical", "Medical Record"),
        ("immunization", "Immunization Card"),
        ("transfer_cert", "Transfer Certificate"),
        ("other", "Other Document"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=30, choices=DOC_TYPES)
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="student_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.admission_number} - {self.title}"


class StudentAcademicHistory(TenantModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="academic_history")
    session_name = models.CharField(max_length=50, help_text="e.g. 2025/2026")
    class_name = models.CharField(max_length=50)
    action = models.CharField(max_length=30, help_text="admitted, promoted, repeated, transferred")
    date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.admission_number} - {self.class_name} ({self.action})"
