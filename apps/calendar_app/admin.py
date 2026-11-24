from django.contrib import admin
from .models import PublicHoliday, SchoolHoliday, AcademicEvent, SchoolAcademicCalendarDocument, CalendarDocumentVersion

admin.site.register(PublicHoliday)
admin.site.register(SchoolHoliday)
admin.site.register(AcademicEvent)
admin.site.register(SchoolAcademicCalendarDocument)
admin.site.register(CalendarDocumentVersion)
