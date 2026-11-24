from rest_framework import serializers
from .models import PublicHoliday, SchoolHoliday, AcademicEvent, SchoolAcademicCalendarDocument, CalendarDocumentVersion

class PublicHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicHoliday
        fields = "__all__"

class SchoolHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class AcademicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicEvent
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class CalendarDocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source="uploaded_by.get_full_name", read_only=True)
    class Meta:
        model = CalendarDocumentVersion
        fields = "__all__"
        read_only_fields = ["school", "uploaded_at"]

class SchoolAcademicCalendarDocumentSerializer(serializers.ModelSerializer):
    versions = CalendarDocumentVersionSerializer(many=True, read_only=True)
    class Meta:
        model = SchoolAcademicCalendarDocument
        fields = "__all__"
        read_only_fields = ["school", "current_version_number", "created_at", "updated_at"]
