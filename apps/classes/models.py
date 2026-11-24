from django.db import models
from apps.core.models import TenantModel, TimeStampedModel

SECTION_CHOICES = [
    ("primary", "Primary"),
    ("secondary", "Secondary"),
]

class ClassLevel(TenantModel):
    name = models.CharField(max_length=50, help_text="e.g. Primary 1, JSS 1, SSS 2")
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    order = models.PositiveIntegerField(default=1, help_text="Order in progression")

    class Meta:
        ordering = ["section", "order", "name"]
        unique_together = ("school", "name")

    def __str__(self):
        return f"{self.name} ({self.get_section_display()})"


class ClassArm(TenantModel):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name="arms")
    name = models.CharField(max_length=50, help_text="e.g. A, B, Gold, Diamond")
    capacity = models.PositiveIntegerField(default=40)

    class Meta:
        ordering = ["class_level__order", "name"]
        unique_together = ("school", "class_level", "name")

    def __str__(self):
        return f"{self.class_level.name} - {self.name}"


class Subject(TenantModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default="secondary")
    is_elective = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("school", "code")

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class SubjectAssignment(TenantModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="subject_assignments")
    teacher = models.ForeignKey("teachers.TeacherProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name="subject_assignments")

    class Meta:
        unique_together = ("school", "subject", "class_arm")

    def __str__(self):
        return f"{self.subject} - {self.class_arm}"


class ClassTeacherAssignment(TenantModel):
    class_arm = models.OneToOneField(ClassArm, on_delete=models.CASCADE, related_name="class_teacher_assignment")
    teacher = models.ForeignKey("teachers.TeacherProfile", on_delete=models.CASCADE, related_name="class_teacher_assignments")

    def __str__(self):
        return f"{self.teacher} -> {self.class_arm}"
