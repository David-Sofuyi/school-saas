from django.db import models
from django.conf import settings
from apps.core.models import TenantModel
from apps.academics.models import AcademicSession, AcademicTerm
from apps.classes.models import ClassLevel
from apps.students.models import Student

class FeeStructure(TenantModel):
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="fee_structures")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name="fee_structures")
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name="fee_structures")
    title = models.CharField(max_length=150, help_text="e.g. JSS 1 First Term 2026/2027 Fee Schedule")
    due_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("school", "term", "class_level")

    def __str__(self):
        return f"{self.title} - {self.class_level.name}"

    @property
    def total_amount(self):
        return sum(item.amount for item in self.items.all())


class FeeItem(TenantModel):
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100, help_text="e.g. Tuition, Development Levy, Uniform, Laboratory")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount in NGN (₦)")
    is_compulsory = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: ₦{self.amount:,.2f}"


class StudentFeeAdjustment(TenantModel):
    ADJUSTMENT_TYPE_CHOICES = [
        ("scholarship", "Scholarship"),
        ("discount", "Special Discount"),
        ("waiver", "Fee Waiver"),
        ("surcharge", "Additional Charge / Extra Lesson"),
        ("other", "Other Authorised Adjustment"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_adjustments")
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name="student_adjustments")
    adjustment_type = models.CharField(max_length=30, choices=ADJUSTMENT_TYPE_CHOICES)
    description = models.CharField(max_length=200, help_text="Reason for discount/surcharge")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Fixed amount in NGN (₦)")
    is_deduction = models.BooleanField(default=True, help_text="True for discounts/scholarships, False for surcharges")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        sign = "-" if self.is_deduction else "+"
        return f"{self.student.admission_number}: {self.get_adjustment_type_display()} ({sign}₦{self.amount:,.2f})"


class StudentInvoice(TenantModel):
    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Fully Paid"),
        ("overdue", "Overdue"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="invoices")
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=50, unique=True)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    adjustments_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpaid")
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    class Meta:
        ordering = ["-issue_date"]
        unique_together = ("school", "student", "fee_structure")

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.student.admission_number} (₦{self.balance_due:,.2f} due)"
