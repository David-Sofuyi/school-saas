from django.contrib import admin

from .models import Announcement, Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "recipient",
        "sender",
        "school",
        "notification_type",
        "channel",
        "is_read",
        "created_at",
    )
    list_filter = ("notification_type", "channel", "is_read", "school", "created_at")
    search_fields = (
        "title",
        "message",
        "recipient__email",
        "recipient__username",
        "sender__email",
    )
    readonly_fields = ("created_at", "read_at")
    date_hierarchy = "created_at"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "school",
        "author",
        "is_published",
        "published_at",
        "expires_at",
        "created_at",
    )
    list_filter = ("is_published", "school", "created_at")
    search_fields = ("title", "content", "author__email", "school__name")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
