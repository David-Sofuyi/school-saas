from rest_framework.routers import DefaultRouter
from .views import StudentAttendanceViewSet, TeacherAttendanceViewSet, TeacherLeaveViewSet

router = DefaultRouter()
router.register("students", StudentAttendanceViewSet, basename="student-attendance")
router.register("teachers", TeacherAttendanceViewSet, basename="teacher-attendance")
router.register("leaves", TeacherLeaveViewSet, basename="teacher-leave")
urlpatterns = router.urls
