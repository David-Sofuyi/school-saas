from rest_framework import serializers
from .models import Timetable, TimetableEntry

class TimetableEntrySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = TimetableEntry
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class TimetableSerializer(serializers.ModelSerializer):
    entries = TimetableEntrySerializer(many=True, read_only=True)
    class_arm_name = serializers.CharField(source="class_arm.__str__", read_only=True)

    class Meta:
        model = Timetable
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]
