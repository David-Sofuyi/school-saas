from rest_framework import serializers
from .models import Student, StudentDocument, StudentAcademicHistory

class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = "__all__"
        read_only_fields = ["school", "uploaded_at"]

class StudentAcademicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAcademicHistory
        fields = "__all__"
        read_only_fields = ["school", "date"]

class StudentSerializer(serializers.ModelSerializer):
    class_arm_name = serializers.CharField(source="current_class_arm.__str__", read_only=True)
    documents = StudentDocumentSerializer(many=True, read_only=True)
    academic_history = StudentAcademicHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]
