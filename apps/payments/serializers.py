from rest_framework import serializers
from .models import SchoolBankAccount, PaymentEvidence, Payment, Receipt

class SchoolBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolBankAccount
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class PaymentEvidenceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    class Meta:
        model = PaymentEvidence
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at", "verified_at", "verified_by"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["school", "created_at", "updated_at"]

class ReceiptSerializer(serializers.ModelSerializer):
    payment_amount = serializers.DecimalField(source="payment.amount", max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = Receipt
        fields = "__all__"
        read_only_fields = ["school", "issue_date", "created_at", "updated_at"]
