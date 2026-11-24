from rest_framework import serializers
from .models import SubscriptionPlan, SchoolSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"

class SchoolSubscriptionSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    class Meta:
        model = SchoolSubscription
        fields = "__all__"
