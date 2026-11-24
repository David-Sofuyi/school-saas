from rest_framework.routers import DefaultRouter
from .views import (
    AcademicSessionViewSet, AcademicTermViewSet, AssessmentComponentViewSet,
    GradeScaleViewSet, StudentScoreViewSet, ResultApprovalViewSet, ReportCardViewSet
)

router = DefaultRouter()
router.register("sessions", AcademicSessionViewSet, basename="session")
router.register("terms", AcademicTermViewSet, basename="term")
router.register("components", AssessmentComponentViewSet, basename="component")
router.register("grade-scales", GradeScaleViewSet, basename="grade-scale")
router.register("scores", StudentScoreViewSet, basename="score")
router.register("approvals", ResultApprovalViewSet, basename="approval")
router.register("report-cards", ReportCardViewSet, basename="report-card")
urlpatterns = router.urls
