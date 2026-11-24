from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.students.models import Student, StudentDocument, StudentAcademicHistory
from apps.students.serializers import StudentSerializer, StudentDocumentSerializer, StudentAcademicHistorySerializer

class StudentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "current_class_arm", "gender"]
    search_fields = ["first_name", "last_name", "admission_number"]

class StudentDocumentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = StudentDocument.objects.all()
    serializer_class = StudentDocumentSerializer
    permission_classes = [IsAuthenticated]

class StudentAcademicHistoryViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = StudentAcademicHistory.objects.all()
    serializer_class = StudentAcademicHistorySerializer
    permission_classes = [IsAuthenticated]
