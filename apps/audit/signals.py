import logging
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver

from .middleware import (
    get_client_ip,
    get_current_request,
    get_current_school,
    get_current_user,
)
from .mixins import get_instance_field_values, log_action
from .models import AuditLog

logger = logging.getLogger(__name__)

# Custom signal for explicit audit logging
audit_event = Signal()  # providing_args: ['action', 'instance', 'user', 'description', 'previous_value', 'new_value', 'school']

# Registry of models that should be audited via signals (if they don't inherit AuditLogMixin)
_REGISTERED_AUDIT_MODELS = set()


def register_audit_model(model_cls):
    """Register a model class to be automatically audited via post_save and post_delete."""
    _REGISTERED_AUDIT_MODELS.add(model_cls)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log successful user login."""
    try:
        school = getattr(request, "school", None) or getattr(user, "school", None)
        ip = get_client_ip(request)
        ua = request.META.get("HTTP_USER_AGENT", "") if request else ""
        AuditLog.objects.create(
            user=user,
            school=school,
            action="login",
            model_name=user._meta.label,
            object_id=str(user.pk),
            object_repr=str(user)[:255],
            description=f"User {user.email} logged in successfully.",
            ip_address=ip,
            user_agent=ua,
        )
    except Exception as exc:
        logger.error(f"Error logging login event: {exc}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout."""
    try:
        if user and user.is_authenticated:
            school = getattr(request, "school", None) or getattr(user, "school", None)
            ip = get_client_ip(request)
            ua = request.META.get("HTTP_USER_AGENT", "") if request else ""
            AuditLog.objects.create(
                user=user,
                school=school,
                action="logout",
                model_name=user._meta.label,
                object_id=str(user.pk),
                object_repr=str(user)[:255],
                description=f"User {user.email} logged out.",
                ip_address=ip,
                user_agent=ua,
            )
    except Exception as exc:
        logger.error(f"Error logging logout event: {exc}")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Log failed login attempt."""
    try:
        email = credentials.get("email") or credentials.get("username") or "Unknown"
        ip = get_client_ip(request)
        ua = request.META.get("HTTP_USER_AGENT", "") if request else ""
        school = getattr(request, "school", None)
        AuditLog.objects.create(
            user=None,
            school=school,
            action="login",
            model_name="accounts.CustomUser",
            object_id="",
            object_repr=email,
            description=f"Failed login attempt for email/username: {email}",
            ip_address=ip,
            user_agent=ua,
        )
    except Exception as exc:
        logger.error(f"Error logging login failure: {exc}")


@receiver(audit_event)
def handle_custom_audit_event(sender, **kwargs):
    """Handle custom audit event signal."""
    try:
        action = kwargs.get("action", "update")
        instance = kwargs.get("instance")
        user = kwargs.get("user")
        description = kwargs.get("description", "")
        previous_value = kwargs.get("previous_value")
        new_value = kwargs.get("new_value")
        school = kwargs.get("school")
        log_action(
            user=user,
            action=action,
            instance=instance,
            previous_value=previous_value,
            new_value=new_value,
            description=description,
            school=school,
        )
    except Exception as exc:
        logger.error(f"Error handling audit_event signal: {exc}")


@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    """Audit post_save for models registered in _REGISTERED_AUDIT_MODELS."""
    # Don't audit AuditLog itself to prevent infinite loops
    if sender is AuditLog or issubclass(sender, AuditLog):
        return
    # Skip if model uses AuditLogMixin (which handles its own save)
    from .mixins import AuditLogMixin
    if isinstance(instance, AuditLogMixin):
        return
    if sender in _REGISTERED_AUDIT_MODELS:
        try:
            action = "create" if created else "update"
            new_val = get_instance_field_values(instance)
            log_action(
                action=action,
                instance=instance,
                previous_value=None if created else None,
                new_value=new_val,
            )
        except Exception as exc:
            logger.error(f"Error in audit_post_save for {sender}: {exc}")


@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    """Audit post_delete for models registered in _REGISTERED_AUDIT_MODELS."""
    if sender is AuditLog or issubclass(sender, AuditLog):
        return
    from .mixins import AuditLogMixin
    if isinstance(instance, AuditLogMixin):
        return
    if sender in _REGISTERED_AUDIT_MODELS:
        try:
            prev_val = get_instance_field_values(instance)
            log_action(
                action="delete",
                instance=instance,
                previous_value=prev_val,
                new_value=None,
            )
        except Exception as exc:
            logger.error(f"Error in audit_post_delete for {sender}: {exc}")
