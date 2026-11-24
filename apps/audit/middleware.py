import threading
from django.utils.deprecation import MiddlewareMixin

_thread_locals = threading.local()


def get_current_request():
    """Return the current HttpRequest from thread-local storage."""
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """Return the current authenticated user from thread-local request, if any."""
    request = get_current_request()
    if request and hasattr(request, "user") and request.user.is_authenticated:
        return request.user
    return None


def get_current_school():
    """Return the current school attached to request, if any."""
    request = get_current_request()
    if request:
        return getattr(request, "school", None)
    return None


def get_client_ip(request):
    """Extract client IP address from request META headers."""
    if not request:
        return None
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware that captures request information (user, IP, user agent)
    into thread-local storage so that model mixins and signal handlers
    can seamlessly log audit trails.
    """

    def process_request(self, request):
        _thread_locals.request = request
        return None

    def process_response(self, request, response):
        _thread_locals.request = None
        return response

    def process_exception(self, request, exception):
        _thread_locals.request = None
        return None
