from django.contrib import admin
from .models import FeeStructure, FeeItem, StudentFeeAdjustment, StudentInvoice

class FeeItemInline(admin.TabularInline):
    model = FeeItem
    extra = 1

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ["title", "term", "class_level", "due_date", "is_published", "school"]
    inlines = [FeeItemInline]

admin.site.register(StudentFeeAdjustment)
admin.site.register(StudentInvoice)
