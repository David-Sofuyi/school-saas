from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, SchoolSubscriptionViewSet

router = DefaultRouter()
router.register("plans", SubscriptionPlanViewSet, basename="subscription-plan")
router.register("schools", SchoolSubscriptionViewSet, basename="school-subscription")
urlpatterns = router.urls
