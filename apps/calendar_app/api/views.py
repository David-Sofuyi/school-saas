from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.mixins import TenantQuerySetMixin, TenantCreateMixin
from apps.calendar_app.models import PublicHoliday, SchoolHoliday, AcademicEvent, SchoolAcademicCalendarDocument, CalendarDocumentVersion
from apps.calendar_app.serializers import (
    PublicHolidaySerializer, SchoolHolidaySerializer, AcademicEventSerializer,
    SchoolAcademicCalendarDocumentSerializer, CalendarDocumentVersionSerializer
)

class PublicHolidayViewSet(viewsets.ModelViewSet):
    queryset = PublicHoliday.objects.all()
    serializer_class = PublicHolidaySerializer
    permission_classes = [IsAuthenticated]

class SchoolHolidayViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = SchoolHoliday.objects.all()
    serializer_class = SchoolHolidaySerializer
    permission_classes = [IsAuthenticated]

class AcademicEventViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = AcademicEvent.objects.all()
    serializer_class = AcademicEventSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["category", "session", "term", "status", "target_audience"]

class CalendarDocumentViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = SchoolAcademicCalendarDocument.objects.all()
    serializer_class = SchoolAcademicCalendarDocumentSerializer
    permission_classes = [IsAuthenticated]

class CalendarVersionViewSet(TenantQuerySetMixin, TenantCreateMixin, viewsets.ModelViewSet):
    queryset = CalendarDocumentVersion.objects.all()
    serializer_class = CalendarDocumentVersionSerializer
    permission_classes = [IsAuthenticated]
