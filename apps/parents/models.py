from django.db import models
from django.conf import settings
from apps.core.models import TenantModel
from apps.students.models import Student

RELATIONSHIP_CHOICES = [
    ("father", "Father"),
    ("mother", "Mother"),
    ("guardian", "Guardian"),
    ("sponsor", "Sponsor"),
]

class ParentProfile(TenantModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parent_profile")
    occupation = models.CharField(max_length=100, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)
    residential_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Parent)"


class ParentStudent(TenantModel):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name="linked_children")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="linked_parents")
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default="guardian")
    is_emergency_contact = models.BooleanField(default=True)
    is_fee_payer = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "parent", "student")

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.parent.school_id != self.student.school_id:
            raise ValidationError("Parent and student must belong to the exact same school tenant.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.user.get_full_name()} -> {self.student.full_name}"
