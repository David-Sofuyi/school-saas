from rest_framework import serializers
from .models import ParentProfile, ParentStudent
from apps.accounts.serializers import UserSerializer
from apps.students.serializers import StudentSerializer

class ParentProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source="user", read_only=True)
    class Meta:
        model = ParentProfile
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class ParentStudentSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source="student", read_only=True)
    class Meta:
        model = ParentStudent
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]
