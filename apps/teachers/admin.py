from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "staff_id", "employment_status", "employment_date", "school"]
    list_filter = ["employment_status", "school"]
    search_fields = ["user__first_name", "user__last_name", "user__email", "staff_id"]
