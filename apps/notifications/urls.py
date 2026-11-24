from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    # Notifications
    path("", views.NotificationListView.as_view(), name="list"),
    path(
        "<int:pk>/mark-read/",
        views.NotificationMarkReadView.as_view(),
        name="mark_read",
    ),
    path(
        "mark-all-read/",
        views.NotificationMarkReadView.as_view(),
        name="mark_all_read",
    ),
    # Announcements
    path(
        "announcements/",
        views.AnnouncementListView.as_view(),
        name="announcement_list",
    ),
    path(
        "announcements/create/",
        views.AnnouncementCreateView.as_view(),
        name="announcement_create",
    ),
    path(
        "announcements/<int:pk>/",
        views.AnnouncementDetailView.as_view(),
        name="announcement_detail",
    ),
]
