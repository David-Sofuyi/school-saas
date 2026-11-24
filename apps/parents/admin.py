from django.contrib import admin
from .models import ParentProfile, ParentStudent

class ParentStudentInline(admin.TabularInline):
    model = ParentStudent
    extra = 1

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "occupation", "school"]
    list_filter = ["school"]
    inlines = [ParentStudentInline]

admin.site.register(ParentStudent)
