from django.contrib import admin
from .models import AcademicSession, AcademicTerm, AssessmentComponent, GradeScale, StudentScore, ResultApproval, ReportCard

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_current", "school"]

@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ["session", "term_type", "opening_date", "closing_date", "is_current", "school"]

@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ["grade", "min_score", "max_score", "remark", "school"]

@admin.register(StudentScore)
class StudentScoreAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "term", "ca_score", "exam_score", "total_score", "grade", "school"]
    search_fields = ["student__admission_number", "student__last_name"]
    list_filter = ["term", "subject", "school"]

admin.site.register(AssessmentComponent)
admin.site.register(ResultApproval)
admin.site.register(ReportCard)
