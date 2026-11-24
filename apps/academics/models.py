from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import TenantModel
from apps.students.models import Student
from apps.classes.models import ClassArm, Subject

class AcademicSession(TenantModel):
    name = models.CharField(max_length=50, help_text="e.g. 2026/2027")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]
        unique_together = ("school", "name")

    def __str__(self):
        return f"{self.name} ({'Current' if self.is_current else 'Inactive'})"

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.filter(school=self.school, is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class AcademicTerm(TenantModel):
    TERM_CHOICES = [
        ("first", "First Term"),
        ("second", "Second Term"),
        ("third", "Third Term"),
    ]
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="terms")
    term_type = models.CharField(max_length=20, choices=TERM_CHOICES)
    opening_date = models.DateField()
    closing_date = models.DateField()
    exam_start_date = models.DateField(null=True, blank=True)
    exam_end_date = models.DateField(null=True, blank=True)
    resumption_date = models.DateField(null=True, blank=True, help_text="Resumption date for next term")
    is_current = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ["session", "opening_date"]
        unique_together = ("school", "session", "term_type")

    def __str__(self):
        return f"{self.session.name} - {self.get_term_type_display()}"

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicTerm.objects.filter(school=self.school, is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class AssessmentComponent(TenantModel):
    name = models.CharField(max_length=100, help_text="e.g. Class Test 1, Assignment, Mid-term Test")
    max_marks = models.PositiveIntegerField(help_text="Component mark weight")
    section = models.CharField(max_length=20, choices=[("primary", "Primary"), ("secondary", "Secondary"), ("all", "All Sections")], default="all")

    class Meta:
        ordering = ["name"]
        unique_together = ("school", "name", "section")

    def __str__(self):
        return f"{self.name} ({self.max_marks} marks) - {self.section}"


class GradeScale(TenantModel):
    grade = models.CharField(max_length=5, help_text="A, B, C, D, E, F")
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    remark = models.CharField(max_length=50, help_text="Distinction, Excellent, Credit, Pass, Fail")
    is_pass = models.BooleanField(default=True)
    section = models.CharField(max_length=20, choices=[("primary", "Primary"), ("secondary", "Secondary"), ("all", "All")], default="all")

    class Meta:
        ordering = ["-min_score"]
        unique_together = ("school", "grade", "section")

    def __str__(self):
        return f"{self.grade} ({self.min_score}-{self.max_score}%): {self.remark}"


class StudentScore(TenantModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="scores")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="scores")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name="scores")
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="scores")
    ca_breakdown = models.JSONField(default=dict, blank=True, help_text="Component-wise marks e.g. {'Test 1': 15, 'Assignment': 10}")
    ca_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Compulsory max: 40")
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Compulsory max: 60")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Max 100")
    grade = models.CharField(max_length=5, blank=True)
    teacher_remark = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("school", "student", "subject", "term")
        ordering = ["student", "subject"]

    def clean(self):
        if self.ca_score > 40:
            raise ValidationError("Continuous Assessment (CA) score cannot exceed 40 marks as mandated by PRD Section 11.1.")
        if self.exam_score > 60:
            raise ValidationError("Examination score cannot exceed 60 marks as mandated by PRD Section 11.1.")

    def save(self, *args, **kwargs):
        self.clean()
        self.total_score = self.ca_score + self.exam_score
        # Compute grade based on GradeScale
        matching_grade = GradeScale.objects.filter(
            school=self.school,
            min_score__lte=self.total_score,
            max_score__gte=self.total_score
        ).first()
        if matching_grade:
            self.grade = matching_grade.grade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.admission_number} - {self.subject.name}: {self.total_score}% ({self.grade})"


class ResultApproval(TenantModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted for Approval"),
        ("approved", "Approved"),
        ("published", "Published & Locked"),
    ]
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name="approvals")
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="approvals")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    submitted_by = models.ForeignKey("teachers.TeacherProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name="submitted_results")
    approved_by = models.ForeignKey("teachers.TeacherProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_results")
    published_at = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("school", "term", "class_arm")

    def __str__(self):
        return f"{self.class_arm} - {self.term} ({self.get_status_display()})"


class ReportCard(TenantModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="report_cards")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="report_cards")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name="report_cards")
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="report_cards", null=True, blank=True)
    total_marks_obtained = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_marks_possible = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    class_position = models.PositiveIntegerField(null=True, blank=True)
    times_present = models.PositiveIntegerField(default=0)
    times_absent = models.PositiveIntegerField(default=0)
    teacher_remarks = models.TextField(blank=True)
    principal_remarks = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("school", "student", "term")
        ordering = ["-session__start_date", "term", "class_position"]

    def __str__(self):
        return f"Report Card: {self.student.admission_number} - {self.term}"
