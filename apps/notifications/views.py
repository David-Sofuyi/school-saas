from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from .models import Announcement, Notification
from .services import NotificationService


class NotificationListView(LoginRequiredMixin, ListView):
    """Display in-app notifications for the logged-in user."""

    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        filter_type = self.request.GET.get("type")
        if filter_type:
            qs = qs.filter(notification_type=filter_type)
        unread_only = self.request.GET.get("unread")
        if unread_only == "1":
            qs = qs.filter(is_read=False)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unread_count"] = NotificationService.get_unread_count(self.request.user)
        return context


class NotificationMarkReadView(LoginRequiredMixin, View):
    """Mark a single notification or all notifications as read."""

    def post(self, request, *args, **kwargs):
        notification_id = kwargs.get("pk")
        if notification_id:
            notification = get_object_or_404(
                Notification, pk=notification_id, recipient=request.user
            )
            notification.mark_as_read()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "status": "success",
                        "unread_count": NotificationService.get_unread_count(request.user),
                    }
                )
            messages.success(request, "Notification marked as read.")
        else:
            NotificationService.mark_all_as_read(request.user)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"status": "success", "unread_count": 0})
            messages.success(request, "All notifications marked as read.")

        next_url = request.POST.get("next") or request.GET.get("next") or "notifications:list"
        return redirect(next_url)


class AnnouncementListView(LoginRequiredMixin, ListView):
    """Display school announcements."""

    model = Announcement
    template_name = "notifications/announcement_list.html"
    context_object_name = "announcements"
    paginate_by = 15

    def get_queryset(self):
        user = self.request.user
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if not school:
            return Announcement.objects.none()

        qs = Announcement.objects.filter(school=school)

        is_staff_user = getattr(user, "is_platform_superuser", False) or getattr(
            user, "user_type", None
        ) in {"proprietor", "admin", "principal"}

        if not is_staff_user:
            # End-users only see published, non-expired announcements
            now = timezone.now()
            qs = qs.filter(is_published=True).filter(
                models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now)
            )
            # Filter by audience
            user_type = getattr(user, "user_type", "")
            # target_audience contains user_type or 'all'
            qs = [
                ann
                for ann in qs
                if "all" in ann.target_audience or user_type in ann.target_audience
            ]
            return qs

        return qs.order_by("-created_at")


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    """Display single announcement detail."""

    model = Announcement
    template_name = "notifications/announcement_detail.html"
    context_object_name = "announcement"

    def get_queryset(self):
        user = self.request.user
        school = getattr(self.request, "school", None) or getattr(user, "school", None)
        if not school:
            return Announcement.objects.none()
        return Announcement.objects.filter(school=school)


class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new school announcement."""

    model = Announcement
    fields = ["title", "content", "target_audience", "is_published", "expires_at", "attachment"]
    template_name = "notifications/announcement_form.html"
    success_url = reverse_lazy("notifications:announcement_list")

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "is_platform_superuser", False) or user.is_superuser:
            return True
        return getattr(user, "user_type", None) in {"proprietor", "admin", "principal"}

    def form_valid(self, form):
        school = getattr(self.request, "school", None) or getattr(self.request.user, "school", None)
        if not school:
            messages.error(self.request, "No school context found.")
            return redirect("notifications:announcement_list")

        form.instance.school = school
        form.instance.author = self.request.user
        if form.instance.is_published:
            form.instance.published_at = timezone.now()

        response = super().form_valid(form)

        if form.instance.is_published:
            # Dispatch notifications to the target audience
            NotificationService.publish_announcement(self.object)

        messages.success(self.request, "Announcement created successfully.")
        return response
