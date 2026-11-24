from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentDocumentViewSet, StudentAcademicHistoryViewSet

router = DefaultRouter()
router.register("records", StudentViewSet, basename="student")
router.register("documents", StudentDocumentViewSet, basename="student-document")
router.register("history", StudentAcademicHistoryViewSet, basename="student-history")
urlpatterns = router.urls
