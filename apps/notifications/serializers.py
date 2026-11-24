from rest_framework import serializers

from .models import Announcement, Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    notification_type_display = serializers.CharField(
        source="get_notification_type_display", read_only=True
    )
    channel_display = serializers.CharField(
        source="get_channel_display", read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "school",
            "recipient",
            "sender",
            "sender_name",
            "notification_type",
            "notification_type_display",
            "title",
            "message",
            "channel",
            "channel_display",
            "is_read",
            "read_at",
            "link",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "read_at",
            "notification_type_display",
            "channel_display",
            "sender_name",
        ]

    def get_sender_name(self, obj):
        if obj.sender:
            return obj.sender.get_full_name() or obj.sender.username or obj.sender.email
        return "System"


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    school_name = serializers.CharField(source="school.name", read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            "id",
            "school",
            "school_name",
            "title",
            "content",
            "author",
            "author_name",
            "target_audience",
            "is_published",
            "published_at",
            "expires_at",
            "attachment",
            "is_expired",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "author_name",
            "school_name",
            "is_expired",
        ]

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username or obj.author.email
        return None
