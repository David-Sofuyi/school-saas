from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.teachers.models import TeacherProfile
from apps.teachers.serializers import TeacherProfileSerializer

class TeacherProfileViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]
