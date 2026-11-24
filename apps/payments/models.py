from django.db import models
from django.conf import settings
from apps.core.models import TenantModel
from apps.students.models import Student
from apps.fees.models import StudentInvoice

PAYMENT_STATUS_CHOICES = [
    ("pending", "Pending Verification"),
    ("under_review", "Under Review"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("resubmission_required", "Resubmission Required"),
]

class SchoolBankAccount(TenantModel):
    bank_name = models.CharField(max_length=100, help_text="e.g. Zenith Bank, Access Bank, GTBank, First Bank")
    account_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=20)
    account_purpose = models.CharField(max_length=100, blank=True, help_text="e.g. Tuition Fees, Development, General")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number} ({self.account_name})"


class PaymentEvidence(TenantModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payment_evidences")
    invoice = models.ForeignKey(StudentInvoice, on_delete=models.CASCADE, related_name="payment_evidences")
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount paid in NGN (₦)")
    payment_date = models.DateField()
    bank_used = models.CharField(max_length=100, help_text="Bank paid from or branch")
    transaction_reference = models.CharField(max_length=100, help_text="Teller / Transfer / Session ID")
    evidence_file = models.FileField(upload_to="payment_evidence/", help_text="Image or PDF receipt")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="uploaded_payments")
    status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default="pending")
    reviewer_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_evidences")
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Evidence: {self.transaction_reference} - ₦{self.amount_paid:,.2f} ({self.get_status_display()})"


class Payment(TenantModel):
    invoice = models.ForeignKey(StudentInvoice, on_delete=models.CASCADE, related_name="payments")
    evidence = models.OneToOneField(PaymentEvidence, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_payment")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    reference = models.CharField(max_length=100, unique=True)
    is_reversed = models.BooleanField(default=False)
    reversal_reason = models.TextField(blank=True)
    reversal_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reversed_payments")

    def __str__(self):
        return f"Payment ₦{self.amount:,.2f} ({self.reference})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.is_reversed:
            # Update invoice balance
            self.invoice.amount_paid += self.amount
            self.invoice.balance_due = max(0, self.invoice.net_amount - self.invoice.amount_paid)
            if self.invoice.balance_due == 0:
                self.invoice.status = "paid"
            else:
                self.invoice.status = "partially_paid"
            self.invoice.save()


class Receipt(TenantModel):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="receipt")
    receipt_number = models.CharField(max_length=50, unique=True, help_text="e.g. REC-2026-0001")
    issue_date = models.DateField(auto_now_add=True)
    receipt_file = models.FileField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number} (₦{self.payment.amount:,.2f})"
