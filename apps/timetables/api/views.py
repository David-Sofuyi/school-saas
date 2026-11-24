from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.timetables.models import Timetable, TimetableEntry
from apps.timetables.serializers import TimetableSerializer, TimetableEntrySerializer

class TimetableViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["class_arm", "session", "term", "is_active"]

class TimetableEntryViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = TimetableEntry.objects.all()
    serializer_class = TimetableEntrySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["timetable", "day_of_week", "teacher"]
