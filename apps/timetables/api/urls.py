from rest_framework.routers import DefaultRouter
from .views import TimetableViewSet, TimetableEntryViewSet

router = DefaultRouter()
router.register("schedules", TimetableViewSet, basename="timetable")
router.register("entries", TimetableEntryViewSet, basename="timetable-entry")
urlpatterns = router.urls
