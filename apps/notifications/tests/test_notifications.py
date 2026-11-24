from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.notifications.backends import EmailBackend, InAppBackend, SMSBackend
from apps.notifications.models import Announcement, Notification
from apps.notifications.services import NotificationService
from apps.schools.models import School

User = get_user_model()


class NotificationModelAndServiceTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(
            name="Corona Secondary School",
            slug="corona-sec",
            address="Lekki Phase 1, Lagos",
            city="Lagos",
            state="Lagos",
            contact_phone="+2348033334444",
            contact_email="info@corona.edu.ng",
            school_type="secondary",
        )
        self.teacher = User.objects.create_user(
            email="teacher@corona.edu.ng",
            username="teacher_c",
            password="testpassword123",
            user_type="teacher",
            school=self.school,
            phone_number="08033334444",
        )
        self.student = User.objects.create_user(
            email="student@corona.edu.ng",
            username="student_c",
            password="testpassword123",
            user_type="student",
            school=self.school,
            phone_number="08055556666",
        )

    def test_in_app_notification_creation_and_mark_read(self):
        notification = NotificationService.send_notification(
            recipient=self.student,
            title="Assignment Due",
            message="Mathematics assignment is due tomorrow.",
            notification_type="academic",
            channel="in_app",
            sender=self.teacher,
        )
        self.assertEqual(Notification.objects.count(), 1)
        self.assertFalse(notification.is_read)
        self.assertEqual(NotificationService.get_unread_count(self.student), 1)

        NotificationService.mark_as_read(notification.id, self.student)
        self.assertEqual(NotificationService.get_unread_count(self.student), 0)

    def test_bulk_notification_service(self):
        recipients = [self.teacher, self.student]
        created = NotificationService.send_bulk_notification(
            recipients=recipients,
            title="School Assembly",
            message="Assembly begins at 8:00 AM prompt.",
            notification_type="announcement",
            channel="in_app",
            school=self.school,
        )
        self.assertEqual(len(created), 2)
        self.assertEqual(NotificationService.get_unread_count(self.teacher), 1)
        self.assertEqual(NotificationService.get_unread_count(self.student), 1)

    def test_email_backend(self):
        backend = EmailBackend()
        sent = backend.send(
            recipient=self.teacher,
            title="Staff Meeting",
            message="Staff meeting at 3:00 PM today.",
        )
        self.assertTrue(sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Staff Meeting")

    def test_sms_backend_termii_formatting(self):
        sms_backend = SMSBackend()
        formatted = sms_backend.format_phone_number("08033334444")
        self.assertEqual(formatted, "2348033334444")

        # Test mock send without API key configured
        res = sms_backend.send(
            recipient=self.teacher,
            title="Alert",
            message="School gate closed.",
        )
        self.assertTrue(res)

    def test_announcement_publish_triggers_notifications(self):
        announcement = Announcement.objects.create(
            school=self.school,
            title="Mid-term Break Announcement",
            content="Mid-term break starts on Thursday.",
            author=self.teacher,
            target_audience=["all"],
            is_published=False,
        )
        notif_count = NotificationService.publish_announcement(announcement)
        self.assertTrue(announcement.is_published)
        self.assertIsNotNone(announcement.published_at)
        self.assertEqual(notif_count, 2)  # teacher and student


class NotificationApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(
            name="Greenwood College",
            slug="greenwood-college",
            address="Victoria Island, Lagos",
            city="Lagos",
            state="Lagos",
            contact_phone="+2348077778888",
            contact_email="admin@greenwood.edu.ng",
            school_type="secondary",
        )
        self.user = User.objects.create_user(
            email="user@greenwood.edu.ng",
            username="greenwood_user",
            password="testpassword123",
            user_type="teacher",
            school=self.school,
        )
        self.notif1 = Notification.objects.create(
            recipient=self.user,
            school=self.school,
            title="Notice 1",
            message="Message 1",
        )
        self.notif2 = Notification.objects.create(
            recipient=self.user,
            school=self.school,
            title="Notice 2",
            message="Message 2",
        )

    def test_get_notifications_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/notifications/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_unread_count_endpoint(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/notifications/items/unread-count/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 2)

    def test_mark_read_action(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f"/api/v1/notifications/items/{self.notif1.id}/mark-read/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notif1.refresh_from_db()
        self.assertTrue(self.notif1.is_read)
        self.assertEqual(response.data["unread_count"], 1)

    def test_mark_all_read_action(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/v1/notifications/items/mark-all-read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(NotificationService.get_unread_count(self.user), 0)
