from rest_framework.routers import DefaultRouter
from .views import (
    ClassLevelViewSet, ClassArmViewSet, SubjectViewSet,
    SubjectAssignmentViewSet, ClassTeacherAssignmentViewSet
)

router = DefaultRouter()
router.register("levels", ClassLevelViewSet, basename="class-level")
router.register("arms", ClassArmViewSet, basename="class-arm")
router.register("subjects", SubjectViewSet, basename="subject")
router.register("subject-assignments", SubjectAssignmentViewSet, basename="subject-assignment")
router.register("class-teachers", ClassTeacherAssignmentViewSet, basename="class-teacher")

urlpatterns = router.urls
