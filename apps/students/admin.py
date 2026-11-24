from django.contrib import admin
from .models import Student, StudentDocument, StudentAcademicHistory

class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 1

class StudentAcademicHistoryInline(admin.TabularInline):
    model = StudentAcademicHistory
    extra = 0
    readonly_fields = ["date"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["admission_number", "last_name", "first_name", "current_class_arm", "status", "school"]
    list_filter = ["status", "current_class_arm", "school"]
    search_fields = ["admission_number", "first_name", "last_name"]
    inlines = [StudentDocumentInline, StudentAcademicHistoryInline]
