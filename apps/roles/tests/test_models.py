from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.roles.models import Role, UserRole
from apps.roles.utils import (
    create_default_roles,
    get_user_permissions,
    has_permission,
)
from apps.schools.models import School

User = get_user_model()


class RolesTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(
            name="Greenwood High",
            address="1 Marina St",
            city="Lagos",
            state="Lagos",
            contact_phone="+2348000000001",
            contact_email="admin@greenwood.ng",
            school_type="both",
        )
        self.proprietor_user = User.objects.create_user(
            username="proprietor1",
            email="proprietor@greenwood.ng",
            password="password123",
            user_type="proprietor",
            school=self.school,
        )
        self.teacher_user = User.objects.create_user(
            username="teacher1",
            email="teacher@greenwood.ng",
            password="password123",
            user_type="teacher",
            school=self.school,
        )

    def test_create_default_roles(self):
        roles = create_default_roles(self.school)
        self.assertEqual(len(roles), 5)
        role_names = {r.name for r in roles}
        self.assertSetEqual(
            role_names, {"Proprietor", "Admin", "Principal", "Teacher", "Bursar"}
        )

    def test_permissions_check(self):
        create_default_roles(self.school)
        teacher_role = Role.objects.get(name="Teacher", school=self.school)

        UserRole.objects.create(
            user=self.teacher_user,
            role=teacher_role,
            school=self.school,
            assigned_by=self.proprietor_user,
        )

        # Teacher should have manage_attendance
        self.assertTrue(
            has_permission(self.teacher_user, "manage_attendance", school=self.school)
        )
        # Teacher should NOT have manage_school
        self.assertFalse(
            has_permission(self.teacher_user, "manage_school", school=self.school)
        )

        # Proprietor has all permissions for their school
        self.assertTrue(
            has_permission(self.proprietor_user, "manage_school", school=self.school)
        )
        self.assertTrue(
            has_permission(self.proprietor_user, "manage_fees", school=self.school)
        )

    def test_superuser_has_all_permissions(self):
        superuser = User.objects.create_superuser(
            username="super",
            email="super@domain.ng",
            password="password123",
            user_type="superuser",
            is_platform_superuser=True,
        )
        self.assertTrue(has_permission(superuser, "manage_school", school=self.school))
        self.assertTrue(
            has_permission(superuser, "any_arbitrary_unexisting_perm") is False
        )
