from rest_framework.routers import DefaultRouter
from .views import FeeStructureViewSet, FeeItemViewSet, StudentFeeAdjustmentViewSet, StudentInvoiceViewSet

router = DefaultRouter()
router.register("structures", FeeStructureViewSet, basename="fee-structure")
router.register("items", FeeItemViewSet, basename="fee-item")
router.register("adjustments", StudentFeeAdjustmentViewSet, basename="fee-adjustment")
router.register("invoices", StudentInvoiceViewSet, basename="fee-invoice")
urlpatterns = router.urls
