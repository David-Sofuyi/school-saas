from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.audit.middleware import AuditMiddleware, get_current_request
from apps.audit.mixins import capture_changes, log_action
from apps.audit.models import AuditLog
from apps.schools.models import School

User = get_user_model()


class AuditLogModelTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(
            name="Grace Academy",
            slug="grace-academy",
            address="12 Victoria Island, Lagos",
            city="Lagos",
            state="Lagos",
            contact_phone="+2348012345678",
            contact_email="admin@grace.edu.ng",
            school_type="primary",
        )
        self.user = User.objects.create_user(
            email="teacher@grace.edu.ng",
            username="teacher",
            password="testpassword123",
            user_type="teacher",
            school=self.school,
        )

    def test_create_audit_log_entry(self):
        log = AuditLog.objects.create(
            user=self.user,
            school=self.school,
            action="create",
            model_name="accounts.CustomUser",
            object_id=str(self.user.pk),
            object_repr=str(self.user),
            description="Created user record",
            ip_address="127.0.0.1",
            user_agent="TestClient/1.0",
        )
        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertIn("create", str(log))
        self.assertIn("accounts.CustomUser", str(log))

    def test_log_action_utility(self):
        log = log_action(
            user=self.user,
            action="update",
            instance=self.school,
            previous_value={"name": "Old School Name"},
            new_value={"name": "Grace Academy"},
            description="Updated school name",
        )
        self.assertEqual(log.action, "update")
        self.assertEqual(log.school, self.school)
        self.assertEqual(log.previous_value["name"], "Old School Name")
        self.assertEqual(log.new_value["name"], "Grace Academy")

    def test_audit_middleware_thread_local(self):
        rf = RequestFactory()
        request = rf.get("/api/v1/audit/logs/")
        request.user = self.user

        middleware = AuditMiddleware(get_response=lambda req: "ok")
        middleware.process_request(request)

        current_req = get_current_request()
        self.assertIsNotNone(current_req)
        self.assertEqual(current_req.user, self.user)

        middleware.process_response(request, None)
        self.assertIsNone(get_current_request())


class AuditApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(
            name="Apex College",
            slug="apex-college",
            address="45 Ikeja, Lagos",
            city="Lagos",
            state="Lagos",
            contact_phone="+2348098765432",
            contact_email="admin@apex.edu.ng",
            school_type="secondary",
        )
        self.proprietor = User.objects.create_user(
            email="proprietor@apex.edu.ng",
            username="proprietor",
            password="testpassword123",
            user_type="proprietor",
            school=self.school,
        )
        self.student = User.objects.create_user(
            email="student@apex.edu.ng",
            username="student",
            password="testpassword123",
            user_type="student",
            school=self.school,
        )
        self.log_entry = AuditLog.objects.create(
            user=self.proprietor,
            school=self.school,
            action="login",
            model_name="accounts.CustomUser",
            object_id=str(self.proprietor.pk),
            object_repr=str(self.proprietor),
            description="Proprietor logged in",
        )

    def test_proprietor_can_view_audit_logs(self):
        self.client.force_authenticate(user=self.proprietor)
        response = self.client.get("/api/v1/audit/logs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_student_cannot_view_audit_logs(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get("/api/v1/audit/logs/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
