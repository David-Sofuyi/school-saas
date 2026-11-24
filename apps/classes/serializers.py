from rest_framework import serializers
from .models import ClassLevel, ClassArm, Subject, SubjectAssignment, ClassTeacherAssignment

class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLevel
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class ClassArmSerializer(serializers.ModelSerializer):
    class_level_name = serializers.CharField(source="class_level.name", read_only=True)
    class Meta:
        model = ClassArm
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class SubjectAssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    class_arm_name = serializers.CharField(source="class_arm.__str__", read_only=True)
    class Meta:
        model = SubjectAssignment
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class ClassTeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTeacherAssignment
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]
