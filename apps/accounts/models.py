from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

USER_TYPE_CHOICES = [
    ("superuser", "Platform Superuser"),
    ("proprietor", "School Proprietor"),
    ("admin", "School Administrator"),
    ("principal", "Principal / Head Teacher"),
    ("teacher", "Teacher"),
    ("bursar", "Bursar / Accountant"),
    ("parent", "Parent / Guardian"),
    ("student", "Student"),
]


class CustomUser(AbstractUser):
    """
    Custom user model for the School Management SaaS.

    Uses *email* as the login identifier (``USERNAME_FIELD``).
    """

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    is_platform_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email
