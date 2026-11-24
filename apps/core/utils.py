"""
Helper utilities for the Nigerian School Management SaaS.
"""

from decimal import Decimal


def get_current_school(request):
    """
    Return the current :class:`~apps.schools.models.School` instance attached
    to *request* by ``TenantMiddleware``, or ``None``.
    """
    return getattr(request, "school", None)


def naira_format(amount) -> str:
    """
    Format a numeric *amount* as a Nigerian Naira string.

    >>> naira_format(1000)
    '₦1,000.00'
    >>> naira_format(2500.5)
    '₦2,500.50'
    """
    value = Decimal(str(amount))
    return f"₦{value:,.2f}"


def generate_unique_id(prefix: str, model_class) -> str:
    """
    Generate a zero-padded unique ID with the given *prefix*.

    The function queries ``model_class`` for the current maximum count and
    returns the next value.  Example output: ``'STU-00001'``.

    The ID field on the model is assumed to be the default auto-incrementing
    ``pk``.  The padding width is 5 digits.
    """
    count = model_class.objects.count()
    next_number = count + 1
    return f"{prefix}-{next_number:05d}"
