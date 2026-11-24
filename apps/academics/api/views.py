from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.academics.models import AcademicSession, AcademicTerm, AssessmentComponent, GradeScale, StudentScore, ResultApproval, ReportCard
from apps.academics.serializers import (
    AcademicSessionSerializer, AcademicTermSerializer, AssessmentComponentSerializer,
    GradeScaleSerializer, StudentScoreSerializer, ResultApprovalSerializer, ReportCardSerializer
)

class AcademicSessionViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = [IsAuthenticated]

class AcademicTermViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer
    permission_classes = [IsAuthenticated]

class AssessmentComponentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = AssessmentComponent.objects.all()
    serializer_class = AssessmentComponentSerializer
    permission_classes = [IsAuthenticated]

class GradeScaleViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = GradeScale.objects.all()
    serializer_class = GradeScaleSerializer
    permission_classes = [IsAuthenticated]

class StudentScoreViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = StudentScore.objects.all()
    serializer_class = StudentScoreSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["student", "subject", "term", "class_arm"]

class ResultApprovalViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = ResultApproval.objects.all()
    serializer_class = ResultApprovalSerializer
    permission_classes = [IsAuthenticated]

class ReportCardViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = ReportCard.objects.all()
    serializer_class = ReportCardSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["student", "term", "class_arm"]
