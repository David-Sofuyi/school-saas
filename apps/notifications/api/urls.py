from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnnouncementViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r"items", NotificationViewSet, basename="notification")
router.register(r"announcements", AnnouncementViewSet, basename="announcement")

urlpatterns = [
    path("", include(router.urls)),
]
