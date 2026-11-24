from rest_framework.routers import DefaultRouter
from .views import TeacherProfileViewSet

router = DefaultRouter()
router.register("profiles", TeacherProfileViewSet, basename="teacher-profile")
urlpatterns = router.urls
