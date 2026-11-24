from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.roles.models import PERMISSION_CHOICES, Role, UserRole

User = get_user_model()


class RoleForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(
        choices=PERMISSION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Role
        fields = ["name", "description", "permissions"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class UserRoleAssignForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ["user", "role"]

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        if school:
            self.fields["user"].queryset = User.objects.filter(school=school)
            self.fields["role"].queryset = Role.objects.filter(
                Q(school=school) | Q(school__isnull=True)
            )
