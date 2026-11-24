from rest_framework import serializers
from .models import AcademicSession, AcademicTerm, AssessmentComponent, GradeScale, StudentScore, ResultApproval, ReportCard

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class AcademicTermSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source="session.name", read_only=True)
    class Meta:
        model = AcademicTerm
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class AssessmentComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentComponent
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class GradeScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeScale
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class StudentScoreSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    class Meta:
        model = StudentScore
        fields = "__all__"
        read_only_fields = ["school", "total_score", "grade", "created_at", "updated_at"]

class ResultApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultApproval
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class ReportCardSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    admission_number = serializers.CharField(source="student.admission_number", read_only=True)
    scores = StudentScoreSerializer(source="student.scores", many=True, read_only=True)
    class Meta:
        model = ReportCard
        fields = "__all__"
        read_only_fields = ["school", "generated_at", "created_at", "updated_at"]
