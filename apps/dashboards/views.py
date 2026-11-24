from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.students.models import Student
from apps.teachers.models import TeacherProfile
from apps.fees.models import StudentInvoice
from apps.attendance.models import StudentAttendance
from apps.calendar_app.models import AcademicEvent, SchoolAcademicCalendarDocument

def home_view(request):
    """
    Public front page / landing page for EduNaija SaaS.
    """
    return render(request, "landing.html")

@login_required
def dashboard_router(request):
    """
    Redirects authenticated users to their role-specific dashboard.
    """
    u = request.user
    if u.is_platform_superuser or u.user_type == "superuser":
        return redirect("dashboard-superuser")
    elif u.user_type in ["proprietor", "admin", "bursar"]:
        return redirect("dashboard-proprietor")
    elif u.user_type == "principal":
        return redirect("dashboard-proprietor")
    elif u.user_type == "teacher":
        return redirect("dashboard-teacher")
    elif u.user_type == "parent":
        return redirect("dashboard-parent")
    elif u.user_type == "student":
        return redirect("dashboard-student")
    return render(request, "dashboard/proprietor.html")

@login_required
def superuser_dashboard(request):
    from apps.schools.models import School
    schools_count = School.objects.count()
    active_schools = School.objects.filter(is_active=True).count()
    return render(request, "dashboard/superuser.html", {
        "schools_count": schools_count,
        "active_schools": active_schools,
    })

@login_required
def proprietor_dashboard(request):
    school = getattr(request, "school", None)
    total_students = Student.objects.filter(school=school, status="active").count() if school else 0
    total_teachers = TeacherProfile.objects.filter(school=school, employment_status="active").count() if school else 0
    recent_events = AcademicEvent.objects.filter(school=school, status="published")[:5] if school else []
    return render(request, "dashboard/proprietor.html", {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "recent_events": recent_events,
    })

@login_required
def teacher_dashboard(request):
    school = getattr(request, "school", None)
    return render(request, "dashboard/teacher.html", {"school": school})

@login_required
def parent_dashboard(request):
    school = getattr(request, "school", None)
    parent_profile = getattr(request.user, "parent_profile", None)
    children = []
    if parent_profile:
        children = [link.student for link in parent_profile.linked_children.all()]
    calendars = SchoolAcademicCalendarDocument.objects.filter(school=school, is_published=True, visible_to_parents=True) if school else []
    return render(request, "dashboard/parent.html", {
        "children": children,
        "calendars": calendars,
    })

@login_required
def student_dashboard(request):
    school = getattr(request, "school", None)
    student_profile = getattr(request.user, "student_profile", None)
    calendars = SchoolAcademicCalendarDocument.objects.filter(school=school, is_published=True, visible_to_students=True) if school else []
    return render(request, "dashboard/student.html", {
        "student": student_profile,
        "calendars": calendars,
    })
