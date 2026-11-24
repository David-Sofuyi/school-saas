from rest_framework.routers import DefaultRouter
from .views import ParentProfileViewSet, ParentStudentViewSet

router = DefaultRouter()
router.register("profiles", ParentProfileViewSet, basename="parent-profile")
router.register("links", ParentStudentViewSet, basename="parent-student")
urlpatterns = router.urls
