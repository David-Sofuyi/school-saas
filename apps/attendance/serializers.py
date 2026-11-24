from rest_framework import serializers
from .models import StudentAttendance, TeacherAttendance, TeacherLeave

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    admission_number = serializers.CharField(source="student.admission_number", read_only=True)
    class Meta:
        model = StudentAttendance
        fields = "__all__"
        read_only_fields = ["school", "recorded_at", "recorded_by"]

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)
    class Meta:
        model = TeacherAttendance
        fields = "__all__"
        read_only_fields = ["school", "verified_at"]

class TeacherLeaveSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)
    class Meta:
        model = TeacherLeave
        fields = "__all__"
        read_only_fields = ["school", "approval_date"]
