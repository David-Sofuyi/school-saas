from django.db import models
from apps.core.models import TimeStampedModel
from apps.schools.models import School

class SubscriptionPlan(TimeStampedModel):
    name = models.CharField(max_length=100, help_text="e.g. Starter, Standard, Enterprise")
    code = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    max_students = models.PositiveIntegerField(default=300)
    max_teachers = models.PositiveIntegerField(default=30)
    price_per_term = models.DecimalField(max_digits=12, decimal_places=2, default=50000)
    price_annual = models.DecimalField(max_digits=12, decimal_places=2, default=135000)
    features = models.JSONField(default=list, help_text="List of enabled features")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (₦{self.price_per_term:,.2f}/term)"


class SchoolSubscription(TimeStampedModel):
    STATUS_CHOICES = [
        ("trial", "Trial"),
        ("active", "Active"),
        ("past_due", "Past Due"),
        ("suspended", "Suspended"),
        ("cancelled", "Cancelled"),
    ]
    BILLING_CYCLE_CHOICES = [
        ("termly", "Termly"),
        ("annual", "Annual"),
    ]
    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name="saas_subscription")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name="school_subscriptions")
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES, default="termly")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="trial")
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.school.name} - {self.plan.name} ({self.get_status_display()})"
