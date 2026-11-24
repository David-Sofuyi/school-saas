from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.attendance.models import StudentAttendance, TeacherAttendance, TeacherLeave
from apps.attendance.serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer, TeacherLeaveSerializer

class StudentAttendanceViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["date", "class_arm", "status"]

class TeacherAttendanceViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["date", "teacher", "status", "verification_status"]

class TeacherLeaveViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = TeacherLeave.objects.all()
    serializer_class = TeacherLeaveSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["teacher", "approval_status", "leave_type"]
