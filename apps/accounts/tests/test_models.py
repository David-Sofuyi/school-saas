from django.test import TestCase
from apps.accounts.models import CustomUser


class CustomUserManagerTestCase(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="teacher@example.com",
            username="teacher1",
            password="securepassword123",
            user_type="teacher",
            first_name="Jane",
            last_name="Doe",
        )
        self.assertEqual(user.email, "teacher@example.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_platform_superuser)
        self.assertEqual(user.user_type, "teacher")

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="admin1",
            password="superpassword123",
            first_name="Super",
            last_name="Admin",
        )
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.check_password("superpassword123"))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_platform_superuser)
        self.assertEqual(admin.user_type, "superuser")

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="",
                username="test",
                password="password",
            )
