from django.contrib import admin
from .models import Timetable, TimetableEntry

class TimetableEntryInline(admin.TabularInline):
    model = TimetableEntry
    extra = 1

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ["class_arm", "term", "is_active", "school"]
    inlines = [TimetableEntryInline]

admin.site.register(TimetableEntry)
