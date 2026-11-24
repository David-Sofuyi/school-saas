from django.db import models
from django.conf import settings
from apps.core.models import TenantModel
from apps.students.models import Student
from apps.teachers.models import TeacherProfile
from apps.classes.models import ClassArm

ATTENDANCE_STATUS_CHOICES = [
    ("present", "Present"),
    ("absent", "Absent"),
    ("late", "Late"),
    ("excused", "Excused"),
]

TEACHER_VERIFICATION_CHOICES = [
    ("pending", "Pending Verification"),
    ("verified", "Verified"),
    ("flagged", "Flagged"),
]

class StudentAttendance(TenantModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default="present")
    remarks = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="recorded_student_attendances")
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("school", "student", "date")
        ordering = ["-date", "student__last_name"]
        indexes = [
            models.Index(fields=["school", "date", "status"]),
        ]

    def __str__(self):
        return f"{self.student.admission_number} - {self.date}: {self.get_status_display()}"


class TeacherAttendance(TenantModel):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(db_index=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ("not_checked_in", "Not Checked In"),
        ("present", "Present"),
        ("late", "Late"),
        ("absent", "Absent"),
        ("on_leave", "On Leave"),
        ("excused", "Excused"),
    ], default="not_checked_in")
    verification_status = models.CharField(max_length=20, choices=TEACHER_VERIFICATION_CHOICES, default="pending")
    verification_remarks = models.TextField(blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_teacher_attendances")
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("school", "teacher", "date")
        ordering = ["-date", "teacher__user__first_name"]

    def __str__(self):
        return f"{self.teacher} - {self.date}: {self.get_status_display()} ({self.get_verification_status_display()})"


class TeacherLeave(TenantModel):
    LEAVE_TYPE_CHOICES = [
        ("casual", "Casual Leave"),
        ("sick", "Sick Leave"),
        ("maternity", "Maternity Leave"),
        ("annual", "Annual Leave"),
        ("study", "Study Leave"),
        ("compassionate", "Compassionate Leave"),
    ]
    APPROVAL_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="leave_records")
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default="pending")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves")
    approval_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.teacher} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"
