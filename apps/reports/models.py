from django.db import models
from apps.core.models import TenantModel

class Report(TenantModel):
    name = models.CharField(max_length=150)
    report_type = models.CharField(max_length=30)
    generated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)