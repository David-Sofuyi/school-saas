from django import forms

from apps.schools.models import DAYS_OF_WEEK, School, SchoolSettings


class SchoolRegistrationForm(forms.ModelForm):
    """Form for creating / updating a School."""

    working_days = forms.TypedMultipleChoiceField(
        choices=DAYS_OF_WEEK,
        coerce=int,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select days the school is open.",
    )

    class Meta:
        model = School
        fields = [
            "name",
            "address",
            "city",
            "state",
            "contact_phone",
            "contact_email",
            "website",
            "school_type",
            "opening_time",
            "closing_time",
            "resumption_time",
            "working_days",
            "motto",
            "established_date",
            "logo",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "opening_time": forms.TimeInput(attrs={"type": "time"}),
            "closing_time": forms.TimeInput(attrs={"type": "time"}),
            "resumption_time": forms.TimeInput(attrs={"type": "time"}),
            "established_date": forms.DateInput(attrs={"type": "date"}),
        }


class SchoolSettingsForm(forms.ModelForm):
    """Form for editing SchoolSettings."""

    class Meta:
        model = SchoolSettings
        fields = [
            "enable_sms",
            "enable_email",
            "attendance_reminder_time",
            "absence_notification_time",
            "primary_color",
            "secondary_color",
        ]
        widgets = {
            "attendance_reminder_time": forms.TimeInput(attrs={"type": "time"}),
            "absence_notification_time": forms.TimeInput(attrs={"type": "time"}),
            "primary_color": forms.TextInput(attrs={"type": "color"}),
            "secondary_color": forms.TextInput(attrs={"type": "color"}),
        }
