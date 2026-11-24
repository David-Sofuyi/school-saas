from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.fees.models import FeeStructure, FeeItem, StudentFeeAdjustment, StudentInvoice
from apps.fees.serializers import FeeStructureSerializer, FeeItemSerializer, StudentFeeAdjustmentSerializer, StudentInvoiceSerializer

class FeeStructureViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAuthenticated]

class FeeItemViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = FeeItem.objects.all()
    serializer_class = FeeItemSerializer
    permission_classes = [IsAuthenticated]

class StudentFeeAdjustmentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = StudentFeeAdjustment.objects.all()
    serializer_class = StudentFeeAdjustmentSerializer
    permission_classes = [IsAuthenticated]

class StudentInvoiceViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = StudentInvoice.objects.all()
    serializer_class = StudentInvoiceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "student", "fee_structure"]
