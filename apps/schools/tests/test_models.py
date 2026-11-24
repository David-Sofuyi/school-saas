from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from apps.schools.models import School, SchoolSettings


class SchoolModelTest(TestCase):
    def test_school_creation_and_slug(self):
        school = School.objects.create(
            name="Apex Academy",
            address="123 Broad St",
            city="Lagos",
            state="Lagos",
            contact_phone="+2348012345678",
            contact_email="info@apex.edu.ng",
            school_type="both",
        )
        self.assertEqual(school.slug, "apex-academy")
        self.assertTrue(school.has_primary)
        self.assertTrue(school.has_secondary)
        self.assertEqual(str(school), "Apex Academy")

    def test_school_type_primary(self):
        school = School.objects.create(
            name="Little Stars Nursery",
            address="45 Market Rd",
            city="Ibadan",
            state="Oyo",
            contact_phone="+2348087654321",
            contact_email="admin@littlestars.ng",
            school_type="primary",
        )
        self.assertTrue(school.has_primary)
        self.assertFalse(school.has_secondary)

    def test_school_type_secondary(self):
        school = School.objects.create(
            name="Highland College",
            address="10 Hill Ave",
            city="Enugu",
            state="Enugu",
            contact_phone="+2348099887766",
            contact_email="info@highland.ng",
            school_type="secondary",
        )
        self.assertFalse(school.has_primary)
        self.assertTrue(school.has_secondary)

    def test_subscription_active_property(self):
        school = School.objects.create(
            name="Future Leaders School",
            address="7 Unity Way",
            city="Abuja",
            state="FCT",
            contact_phone="+2348011223344",
            contact_email="info@futureleaders.ng",
            school_type="both",
            subscription_status="active",
            subscription_end=timezone.now().date() + timedelta(days=30),
        )
        self.assertTrue(school.is_subscription_active)

        # Expired date
        school.subscription_end = timezone.now().date() - timedelta(days=1)
        school.save()
        self.assertFalse(school.is_subscription_active)

        # Suspended status
        school.subscription_status = "suspended"
        school.subscription_end = timezone.now().date() + timedelta(days=30)
        school.save()
        self.assertFalse(school.is_subscription_active)


class SchoolSettingsModelTest(TestCase):
    def test_settings_defaults(self):
        school = School.objects.create(
            name="Grace International",
            address="50 Palm St",
            city="Port Harcourt",
            state="Rivers",
            contact_phone="+2348033445566",
            contact_email="contact@grace.ng",
            school_type="both",
        )
        settings = SchoolSettings.objects.create(school=school)
        self.assertEqual(settings.ca_total, 40)
        self.assertEqual(settings.exam_total, 60)
        self.assertTrue(settings.enable_email)
        self.assertFalse(settings.enable_sms)
        self.assertEqual(str(settings), "Settings for Grace International")
