import uuid
from datetime import date, datetime, time
from decimal import Decimal

from django.db import models

from .middleware import (
    get_client_ip,
    get_current_request,
    get_current_school,
    get_current_user,
)


def serialize_value(val):
    """Recursively convert model field values to JSON-serializable types."""
    if val is None:
        return None
    if isinstance(val, (int, float, bool, str)):
        return val
    if isinstance(val, (datetime, date, time)):
        return val.isoformat()
    if isinstance(val, Decimal):
        return str(val)
    if isinstance(val, uuid.UUID):
        return str(val)
    if isinstance(val, (list, tuple)):
        return [serialize_value(x) for x in val]
    if isinstance(val, dict):
        return {str(k): serialize_value(v) for k, v in val.items()}
    if hasattr(val, "pk"):
        return str(val.pk)
    return str(val)


def get_instance_field_values(instance, exclude_fields=None):
    """Extract a dictionary of serializable field values from a model instance."""
    exclude = set(exclude_fields or ["password"])
    values = {}
    for field in instance._meta.concrete_fields:
        if field.name in exclude or field.is_relation and field.many_to_many:
            continue
        try:
            val = getattr(instance, field.name)
            values[field.name] = serialize_value(val)
        except Exception:
            continue
    return values


def capture_changes(instance):
    """
    Compare current instance values against its cached initial state.
    Returns a tuple of (previous_changes, new_changes).
    """
    initial = getattr(instance, "_audit_initial_state", None) or {}
    current = get_instance_field_values(instance)

    if not initial:
        return None, current

    previous_changes = {}
    new_changes = {}

    for key, curr_val in current.items():
        init_val = initial.get(key)
        if init_val != curr_val:
            previous_changes[key] = init_val
            new_changes[key] = curr_val

    return previous_changes, new_changes


def log_action(
    user=None,
    action="create",
    instance=None,
    previous_value=None,
    new_value=None,
    request=None,
    description="",
    school=None,
    model_name=None,
    object_id=None,
    object_repr="",
):
    """
    Create an AuditLog entry. Automatically extracts user, IP, user-agent,
    and school context from thread-local storage if not provided.
    """
    # Lazy import to avoid circular dependency
    from .models import AuditLog

    request = request or get_current_request()

    if user is None:
        if request and hasattr(request, "user") and request.user.is_authenticated:
            user = request.user
        else:
            user = get_current_user()

    if school is None:
        if instance is not None and hasattr(instance, "school"):
            school = instance.school
        elif request is not None and getattr(request, "school", None):
            school = request.school
        elif user is not None and getattr(user, "school", None):
            school = user.school
        else:
            school = get_current_school()

    if instance is not None:
        model_name = model_name or instance._meta.label
        object_id = object_id or str(getattr(instance, "pk", ""))
        object_repr = object_repr or str(instance)[:255]
    else:
        model_name = model_name or "System"
        object_id = str(object_id or "")
        object_repr = object_repr or ""

    ip_address = get_client_ip(request) if request else None
    user_agent = request.META.get("HTTP_USER_AGENT", "") if request else ""

    return AuditLog.objects.create(
        user=user,
        school=school,
        action=action,
        model_name=model_name,
        object_id=object_id,
        object_repr=object_repr,
        previous_value=previous_value,
        new_value=new_value,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
    )


class AuditLogMixin(models.Model):
    """
    Model mixin that automatically captures create, update, and delete actions
    and logs them to the AuditLog table.
    """

    audit_log_enabled = True

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.pk:
            self._audit_initial_state = get_instance_field_values(self)
        else:
            self._audit_initial_state = {}

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._audit_initial_state = get_instance_field_values(instance)
        return instance

    def capture_changes(self):
        """Compare current instance values against the initial state."""
        return capture_changes(self)

    @classmethod
    def log_action(
        cls,
        user=None,
        action="create",
        instance=None,
        previous_value=None,
        new_value=None,
        request=None,
        description="",
        school=None,
    ):
        return log_action(
            user=user,
            action=action,
            instance=instance,
            previous_value=previous_value,
            new_value=new_value,
            request=request,
            description=description,
            school=school,
        )

    def save(self, *args, **kwargs):
        if not getattr(self, "audit_log_enabled", True):
            return super().save(*args, **kwargs)

        is_create = self.pk is None
        if not is_create:
            prev_changes, new_changes = self.capture_changes()
        else:
            prev_changes, new_changes = None, None

        super().save(*args, **kwargs)

        if is_create:
            new_val = get_instance_field_values(self)
            log_action(
                action="create",
                instance=self,
                previous_value=None,
                new_value=new_val,
            )
        elif prev_changes or new_changes:
            log_action(
                action="update",
                instance=self,
                previous_value=prev_changes,
                new_value=new_changes,
            )

        self._audit_initial_state = get_instance_field_values(self)

    def delete(self, *args, **kwargs):
        if not getattr(self, "audit_log_enabled", True):
            return super().delete(*args, **kwargs)

        prev_val = get_instance_field_values(self)
        log_action(
            action="delete",
            instance=self,
            previous_value=prev_val,
            new_value=None,
        )
        return super().delete(*args, **kwargs)
