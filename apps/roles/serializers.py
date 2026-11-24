from rest_framework import serializers

from apps.roles.models import PERMISSION_CHOICES, Role, UserRole


class RoleSerializer(serializers.ModelSerializer):
    permissions_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "school",
            "description",
            "is_system_role",
            "permissions",
            "permissions_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_system_role", "created_at", "updated_at"]

    def get_permissions_display(self, obj):
        choice_dict = dict(PERMISSION_CHOICES)
        return [choice_dict.get(p, p) for p in (obj.permissions or [])]


class UserRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    role_name = serializers.ReadOnlyField(source="role.name")
    school_name = serializers.ReadOnlyField(source="school.name")
    assigned_by_email = serializers.ReadOnlyField(source="assigned_by.email")

    class Meta:
        model = UserRole
        fields = [
            "id",
            "user",
            "user_email",
            "role",
            "role_name",
            "school",
            "school_name",
            "assigned_by",
            "assigned_by_email",
            "assigned_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "assigned_by",
            "assigned_at",
            "created_at",
            "updated_at",
        ]
