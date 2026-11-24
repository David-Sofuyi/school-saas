from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.payments.models import SchoolBankAccount, PaymentEvidence, Payment, Receipt
from apps.payments.serializers import SchoolBankAccountSerializer, PaymentEvidenceSerializer, PaymentSerializer, ReceiptSerializer

class SchoolBankAccountViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = SchoolBankAccount.objects.all()
    serializer_class = SchoolBankAccountSerializer
    permission_classes = [IsAuthenticated]

class PaymentEvidenceViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = PaymentEvidence.objects.all()
    serializer_class = PaymentEvidenceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "student", "invoice"]

class PaymentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

class ReceiptViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]
