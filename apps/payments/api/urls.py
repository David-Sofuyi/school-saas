from rest_framework.routers import DefaultRouter
from .views import SchoolBankAccountViewSet, PaymentEvidenceViewSet, PaymentViewSet, ReceiptViewSet

router = DefaultRouter()
router.register("bank-accounts", SchoolBankAccountViewSet, basename="bank-account")
router.register("evidences", PaymentEvidenceViewSet, basename="payment-evidence")
router.register("records", PaymentViewSet, basename="payment-record")
router.register("receipts", ReceiptViewSet, basename="receipt")
urlpatterns = router.urls
