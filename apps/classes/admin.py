from django.contrib import admin
from .models import ClassLevel, ClassArm, Subject, SubjectAssignment, ClassTeacherAssignment

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ["name", "section", "order", "school"]
    list_filter = ["section", "school"]

@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = ["name", "class_level", "capacity", "school"]
    list_filter = ["class_level", "school"]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "section", "is_elective", "school"]
    search_fields = ["name", "code"]
    list_filter = ["section", "school"]

admin.site.register(SubjectAssignment)
admin.site.register(ClassTeacherAssignment)
