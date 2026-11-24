from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.classes.models import ClassLevel, ClassArm, Subject, SubjectAssignment, ClassTeacherAssignment
from apps.classes.serializers import (
    ClassLevelSerializer, ClassArmSerializer, SubjectSerializer,
    SubjectAssignmentSerializer, ClassTeacherAssignmentSerializer
)

class ClassLevelViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = ClassLevel.objects.all()
    serializer_class = ClassLevelSerializer
    permission_classes = [IsAuthenticated]

class ClassArmViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = ClassArm.objects.all()
    serializer_class = ClassArmSerializer
    permission_classes = [IsAuthenticated]

class SubjectViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class SubjectAssignmentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = SubjectAssignment.objects.all()
    serializer_class = SubjectAssignmentSerializer
    permission_classes = [IsAuthenticated]

class ClassTeacherAssignmentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = ClassTeacherAssignment.objects.all()
    serializer_class = ClassTeacherAssignmentSerializer
    permission_classes = [IsAuthenticated]
