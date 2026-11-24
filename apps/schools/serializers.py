from rest_framework import serializers

from apps.schools.models import School, SchoolSettings


class SchoolSerializer(serializers.ModelSerializer):
    is_subscription_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = School
        fields = "__all__"
        read_only_fields = ("slug", "has_primary", "has_secondary")


class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "slug", "school_type", "city", "state", "is_active"]


class SchoolSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSettings
        fields = "__all__"
        read_only_fields = ("school", "ca_total", "exam_total")
