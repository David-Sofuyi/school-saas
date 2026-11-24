from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.subscriptions.models import SubscriptionPlan, SchoolSubscription
from apps.subscriptions.serializers import SubscriptionPlanSerializer, SchoolSubscriptionSerializer

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]

class SchoolSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = SchoolSubscription.objects.all()
    serializer_class = SchoolSubscriptionSerializer
    permission_classes = [IsAuthenticated]
