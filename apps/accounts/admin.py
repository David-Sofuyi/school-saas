from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "user_type",
        "school",
        "is_platform_superuser",
        "is_staff",
    )
    list_filter = (
        "user_type",
        "is_platform_superuser",
        "is_staff",
        "is_superuser",
        "is_active",
        "school",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "profile_picture")}),
        (
            "School & Role",
            {
                "fields": (
                    "user_type",
                    "school",
                    "is_platform_superuser",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "username", "first_name", "last_name", "phone_number")
    ordering = ("email",)
