from apps.roles.models import PERMISSION_CHOICES, Role, UserRole

DEFAULT_ROLE_PERMISSIONS = {
    "Proprietor": [
        "manage_school",
        "manage_users",
        "manage_students",
        "manage_teachers",
        "manage_parents",
        "manage_classes",
        "manage_subjects",
        "manage_fees",
        "manage_payments",
        "manage_attendance",
        "manage_academics",
        "manage_calendar",
        "manage_events",
        "approve_results",
        "verify_attendance",
        "view_reports",
        "view_financials",
        "manage_timetable",
        "send_notifications",
    ],
    "Admin": [
        "manage_users",
        "manage_students",
        "manage_teachers",
        "manage_parents",
        "manage_classes",
        "manage_subjects",
        "manage_attendance",
        "manage_academics",
        "manage_calendar",
        "manage_events",
        "view_reports",
        "manage_timetable",
        "send_notifications",
    ],
    "Principal": [
        "manage_students",
        "manage_teachers",
        "manage_classes",
        "manage_subjects",
        "manage_attendance",
        "manage_academics",
        "manage_calendar",
        "manage_events",
        "approve_results",
        "verify_attendance",
        "view_reports",
        "manage_timetable",
        "send_notifications",
    ],
    "Teacher": [
        "manage_attendance",
        "manage_academics",
        "manage_calendar",
        "manage_timetable",
    ],
    "Bursar": [
        "manage_fees",
        "manage_payments",
        "view_financials",
        "view_reports",
    ],
}


def create_default_roles(school):
    """
    Creates default system roles for a school with standard permissions.
    """
    created_roles = []
    for role_name, perms in DEFAULT_ROLE_PERMISSIONS.items():
        role, _ = Role.objects.get_or_create(
            name=role_name,
            school=school,
            defaults={
                "description": f"Default {role_name} role for {school.name}",
                "is_system_role": True,
                "permissions": perms,
            },
        )
        created_roles.append(role)
    return created_roles


def get_user_permissions(user, school=None):
    """
    Returns a set of permission codenames that the user holds for the given school.
    If school is None, tries to use user.school.
    Superusers and platform superusers hold all permissions.
    """
    if not user or not user.is_authenticated:
        return set()

    if user.is_superuser or getattr(user, "is_platform_superuser", False):
        return {code for code, _ in PERMISSION_CHOICES}

    target_school = school or getattr(user, "school", None)

    # Proprietor of the school implicitly has all permissions for their school
    if getattr(user, "user_type", None) == "proprietor":
        if target_school and getattr(user, "school", None) == target_school:
            return {code for code, _ in PERMISSION_CHOICES}

    perms = set()
    qs = UserRole.objects.filter(user=user).select_related("role")
    if target_school:
        qs = qs.filter(school=target_school)

    for ur in qs:
        role_perms = ur.role.permissions
        if isinstance(role_perms, list):
            perms.update(role_perms)

    return perms


def has_permission(user, permission_codename, school=None):
    """
    Checks if a user has a specific permission for the given school.
    """
    if not user or not user.is_authenticated:
        return False
    user_perms = get_user_permissions(user, school=school)
    return permission_codename in user_perms
