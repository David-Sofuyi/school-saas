from rest_framework import serializers
from .models import FeeStructure, FeeItem, StudentFeeAdjustment, StudentInvoice

class FeeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeItem
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class FeeStructureSerializer(serializers.ModelSerializer):
    items = FeeItemSerializer(many=True, read_only=True)
    class Meta:
        model = FeeStructure
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class StudentFeeAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeeAdjustment
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class StudentInvoiceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    admission_number = serializers.CharField(source="student.admission_number", read_only=True)
    class Meta:
        model = StudentInvoice
        fields = "__all__"
        read_only_fields = ["school", "issue_date", "created_at", "updated_at"]
