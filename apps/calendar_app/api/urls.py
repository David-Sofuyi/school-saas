from rest_framework.routers import DefaultRouter
from .views import PublicHolidayViewSet, SchoolHolidayViewSet, AcademicEventViewSet, CalendarDocumentViewSet, CalendarVersionViewSet

router = DefaultRouter()
router.register("public-holidays", PublicHolidayViewSet, basename="public-holiday")
router.register("school-holidays", SchoolHolidayViewSet, basename="school-holiday")
router.register("events", AcademicEventViewSet, basename="academic-event")
router.register("documents", CalendarDocumentViewSet, basename="calendar-doc")
router.register("versions", CalendarVersionViewSet, basename="calendar-version")
urlpatterns = router.urls
