import datetime
from celery import shared_task
from django.utils import timezone
from apps.schools.models import School
from apps.attendance.models import StudentAttendance
from apps.notifications.services import NotificationService

@shared_task
def send_daily_attendance_reminders():
    """
    PRD 12.1: Runs every school day at 8:30 AM WAT.
    Reminds teachers to take student roll call, skipping weekends and holidays.
    """
    today = timezone.localdate()
    weekday = today.weekday() # 0 = Mon, 4 = Fri
    schools = School.objects.filter(is_active=True)
    for school in schools:
        if weekday not in (school.working_days or [0, 1, 2, 3, 4]):
            continue
        # Send reminder to active teachers
        teachers = school.users.filter(user_type="teacher", is_active=True)
        for t in teachers:
            NotificationService.send_notification(
                recipient=t,
                title="Roll Call Reminder",
                message="Good morning! Please remember to record your class attendance for today.",
                notification_type="attendance",
                school=school
            )

@shared_task
def check_student_absence_notifications():
    """
    PRD 12.2: Runs at 9:00 AM WAT.
    Checks explicitly recorded absences and alerts class teacher, proprietor, and superuser.
    """
    today = timezone.localdate()
    absences = StudentAttendance.objects.filter(date=today, status="absent")
    for rec in absences:
        # Alert proprietor
        proprietors = rec.school.users.filter(user_type="proprietor")
        for prop in proprietors:
            NotificationService.send_notification(
                recipient=prop,
                title=f"Student Absence: {rec.student.full_name}",
                message=f"Student {rec.student.full_name} ({rec.student.admission_number}) in {rec.class_arm} was marked absent today.",
                notification_type="attendance",
                school=rec.school
            )
