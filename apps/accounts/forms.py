from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users via the web interface."""

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing users via the web interface / admin."""

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "school",
            "profile_picture",
        )


class LoginForm(forms.Form):
    """Simple email + password login form."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
