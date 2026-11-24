from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.schools.api.views import SchoolSettingsViewSet, SchoolViewSet

router = DefaultRouter()
router.register(r"schools", SchoolViewSet, basename="school")
router.register(r"school-settings", SchoolSettingsViewSet, basename="school-settings")

urlpatterns = [
    path("", include(router.urls)),
]
