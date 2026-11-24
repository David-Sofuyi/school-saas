from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.mixins import TenantQuerySetMixin

from ..models import Announcement, Notification
from ..serializers import AnnouncementSerializer, NotificationSerializer
from ..services import NotificationService


class IsAnnouncementManagerOrReadOnly(permissions.BasePermission):
    """
    Allow any authenticated tenant user to read published announcements.
    Only school staff/proprietor/superuser may create, update, or delete.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if getattr(request.user, "is_platform_superuser", False) or request.user.is_superuser:
            return True
        user_type = getattr(request.user, "user_type", None)
        return user_type in {"proprietor", "admin", "principal"}


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for interacting with user notifications.
    Users only see and modify their own notifications.
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["notification_type", "is_read", "channel"]
    search_fields = ["title", "message"]
    ordering_fields = ["created_at", "is_read"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            school=getattr(self.request, "school", None) or getattr(self.request.user, "school", None),
        )

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        """Mark a single notification as read."""
        notification = self.get_object()
        notification.mark_as_read()
        return Response(
            {
                "status": "marked as read",
                "unread_count": NotificationService.get_unread_count(request.user),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        """Mark all unread notifications for current user as read."""
        count = NotificationService.mark_all_as_read(request.user)
        return Response(
            {"status": "success", "marked_read_count": count, "unread_count": 0},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        """Return the unread notification count for the authenticated user."""
        count = NotificationService.get_unread_count(request.user)
        return Response({"unread_count": count}, status=status.HTTP_200_OK)


class AnnouncementViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing school announcements.
    """

    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, IsAnnouncementManagerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_published"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_at", "created_at"]
    ordering = ["-published_at", "-created_at"]

    def get_queryset(self):
        user = self.request.user
        qs = Announcement.objects.select_related("school", "author").all()

        # Apply multi-tenant filtering
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if getattr(user, "is_platform_superuser", False) or user.is_superuser:
            if school:
                qs = qs.filter(school=school)
        else:
            if school:
                qs = qs.filter(school=school)
            else:
                return Announcement.objects.none()

        # Non-staff users only see published and unexpired announcements matching audience
        user_type = getattr(user, "user_type", None)
        is_staff = getattr(user, "is_platform_superuser", False) or user_type in {
            "proprietor",
            "admin",
            "principal",
        }

        if not is_staff:
            now = timezone.now()
            qs = qs.filter(is_published=True)
            # Filter non-expired
            qs = qs.exclude(expires_at__isnull=False, expires_at__lte=now)

        return qs

    def perform_create(self, serializer):
        school = getattr(self.request, "school", None) or getattr(self.request.user, "school", None)
        instance = serializer.save(
            author=self.request.user,
            school=school,
        )
        if instance.is_published:
            if not instance.published_at:
                instance.published_at = timezone.now()
                instance.save(update_fields=["published_at"])
            NotificationService.publish_announcement(instance)

    def perform_update(self, serializer):
        was_published = serializer.instance.is_published
        instance = serializer.save()
        if not was_published and instance.is_published:
            if not instance.published_at:
                instance.published_at = timezone.now()
                instance.save(update_fields=["published_at"])
            NotificationService.publish_announcement(instance)
