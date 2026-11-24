from django.contrib import admin

from apps.schools.models import School, SchoolSettings


class SchoolSettingsInline(admin.StackedInline):
    model = SchoolSettings
    can_delete = False
    verbose_name_plural = "Settings"


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "school_type",
        "city",
        "state",
        "subscription_status",
        "is_active",
    )
    list_filter = ("school_type", "subscription_status", "is_active", "state")
    search_fields = ("name", "slug", "city")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SchoolSettingsInline]


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ("school", "enable_sms", "enable_email", "primary_color")
    list_select_related = ("school",)
