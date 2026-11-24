import logging
from django.contrib.auth import get_user_model
from django.utils import timezone

from .backends import get_notification_backend
from .models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationService:
    """
    Central service layer for dispatching, marking, and querying notifications.
    """

    @classmethod
    def send_notification(
        cls,
        recipient,
        title,
        message,
        notification_type="info",
        channel="in_app",
        school=None,
        sender=None,
        link="",
        **kwargs,
    ):
        """
        Send a notification to a single recipient through the requested channel.
        """
        if school is None:
            school = getattr(recipient, "school", None)

        backend = get_notification_backend(channel)
        result = backend.send(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            school=school,
            sender=sender,
            link=link,
            **kwargs,
        )
        return result

    @classmethod
    def send_bulk_notification(
        cls,
        recipients,
        title,
        message,
        notification_type="info",
        channel="in_app",
        school=None,
        sender=None,
        link="",
        **kwargs,
    ):
        """
        Send notifications to multiple recipients.
        For in_app, uses bulk_create for maximum database performance.
        """
        if channel == "in_app":
            records = []
            for recipient in recipients:
                recip_school = school or getattr(recipient, "school", None)
                records.append(
                    Notification(
                        recipient=recipient,
                        school=recip_school,
                        sender=sender,
                        notification_type=notification_type,
                        title=title,
                        message=message,
                        channel="in_app",
                        link=link,
                    )
                )
            created = Notification.objects.bulk_create(records)
            return created

        backend = get_notification_backend(channel)
        results = []
        for recipient in recipients:
            res = backend.send(
                recipient=recipient,
                title=title,
                message=message,
                notification_type=notification_type,
                school=school or getattr(recipient, "school", None),
                sender=sender,
                link=link,
                **kwargs,
            )
            results.append(res)
        return results

    @classmethod
    def mark_as_read(cls, notification_id, user):
        """Mark a specific notification as read for the user."""
        try:
            notification = Notification.objects.get(pk=notification_id, recipient=user)
            if not notification.is_read:
                notification.is_read = True
                notification.read_at = timezone.now()
                notification.save(update_fields=["is_read", "read_at"])
            return notification
        except Notification.DoesNotExist:
            return None

    @classmethod
    def mark_all_as_read(cls, user):
        """Mark all unread notifications for a user as read."""
        now = timezone.now()
        count = Notification.objects.filter(recipient=user, is_read=False).update(
            is_read=True, read_at=now
        )
        return count

    @classmethod
    def get_unread_count(cls, user):
        """Return the number of unread notifications for a user."""
        if not user or not user.is_authenticated:
            return 0
        return Notification.objects.filter(recipient=user, is_read=False).count()

    @classmethod
    def publish_announcement(cls, announcement):
        """
        Publish an announcement and dispatch in-app notifications
        to all users matching the target_audience for the announcement's school.
        """
        announcement.is_published = True
        announcement.published_at = timezone.now()
        announcement.save(update_fields=["is_published", "published_at"])

        target_audience = announcement.target_audience or ["all"]
        school = announcement.school

        users_qs = User.objects.filter(school=school, is_active=True)
        if "all" not in target_audience:
            users_qs = users_qs.filter(user_type__in=target_audience)

        recipients = list(users_qs)
        if recipients:
            cls.send_bulk_notification(
                recipients=recipients,
                title=f"Announcement: {announcement.title}",
                message=announcement.content[:500],
                notification_type="announcement",
                channel="in_app",
                school=school,
                sender=announcement.author,
            )
        return len(recipients)
