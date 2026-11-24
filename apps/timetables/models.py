from django.db import models
from apps.core.models import TenantModel
from apps.classes.models import ClassArm, Subject
from apps.teachers.models import TeacherProfile
from apps.academics.models import AcademicSession, AcademicTerm

DAYS_OF_WEEK = [
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
]

class Timetable(TenantModel):
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE, related_name="timetables")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="timetables")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name="timetables")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "class_arm", "session", "term")

    def __str__(self):
        return f"{self.class_arm} Timetable - {self.term}"


class TimetableEntry(TenantModel):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name="entries")
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    period_number = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetable_entries")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="timetable_entries")
    classroom = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["day_of_week", "period_number"]
        unique_together = ("timetable", "day_of_week", "period_number")

    def __str__(self):
        return f"{self.get_day_of_week_display()} P{self.period_number}: {self.subject.name}"
