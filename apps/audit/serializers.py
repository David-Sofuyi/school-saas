from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for reading AuditLog records."""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.SerializerMethodField()
    school_name = serializers.CharField(source="school.name", read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "school",
            "school_name",
            "action",
            "action_display",
            "model_name",
            "object_id",
            "object_repr",
            "previous_value",
            "new_value",
            "description",
            "ip_address",
            "user_agent",
            "timestamp",
        ]
        read_only_fields = fields

    def get_user_full_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username or obj.user.email
        return None
