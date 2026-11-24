from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance, TeacherLeave

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ["student", "date", "class_arm", "status", "school"]
    list_filter = ["status", "date", "school"]
    search_fields = ["student__admission_number", "student__last_name"]

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ["teacher", "date", "check_in_time", "check_out_time", "status", "verification_status", "school"]
    list_filter = ["status", "verification_status", "date", "school"]

admin.site.register(TeacherLeave)
