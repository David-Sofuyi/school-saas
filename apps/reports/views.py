from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.students.models import Student
from apps.fees.models import StudentInvoice
from apps.attendance.models import StudentAttendance, TeacherAttendance

@login_required
def academic_reports(request):
    school = getattr(request, "school", None)
    return render(request, "reports/academic.html", {"school": school})

@login_required
def attendance_reports(request):
    school = getattr(request, "school", None)
    return render(request, "reports/attendance.html", {"school": school})

@login_required
def financial_reports(request):
    school = getattr(request, "school", None)
    invoices = StudentInvoice.objects.filter(school=school) if school else []
    total_billed = sum(i.net_amount for i in invoices)
    total_collected = sum(i.amount_paid for i in invoices)
    total_outstanding = sum(i.balance_due for i in invoices)
    return render(request, "reports/financial.html", {
        "total_billed": total_billed,
        "total_collected": total_collected,
        "total_outstanding": total_outstanding,
        "invoices": invoices[:50],
    })

@login_required
def calendar_reports(request):
    school = getattr(request, "school", None)
    return render(request, "reports/calendar.html", {"school": school})
