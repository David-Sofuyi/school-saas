import json
import logging
from abc import ABC, abstractmethod
from urllib import error, parse, request

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class BaseNotificationBackend(ABC):
    """Abstract base class for all notification backends."""

    @abstractmethod
    def send(self, recipient, title, message, **kwargs):
        """
        Send notification to a recipient.

        :param recipient: User model instance
        :param title: Notification headline / email subject
        :param message: Main notification body
        :param kwargs: Optional parameters like school, sender, link, notification_type
        :return: Result object or boolean indicating success
        """
        pass


class InAppBackend(BaseNotificationBackend):
    """
    Creates an in-app Notification database record for the user to view
    on their dashboard and navbar alerts.
    """

    def send(self, recipient, title, message, **kwargs):
        from .models import Notification

        school = kwargs.get("school") or getattr(recipient, "school", None)
        sender = kwargs.get("sender")
        notification_type = kwargs.get("notification_type", "info")
        link = kwargs.get("link", "")

        notification = Notification.objects.create(
            recipient=recipient,
            school=school,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            channel="in_app",
            link=link,
        )
        return notification


class EmailBackend(BaseNotificationBackend):
    """
    Sends email notifications via Django's configured email backend (SMTP / Console).
    """

    def send(self, recipient, title, message, **kwargs):
        email_address = getattr(recipient, "email", None)
        if not email_address:
            logger.warning(
                f"Cannot send email notification: recipient {recipient} has no email address."
            )
            return False

        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@schoolsaas.ng")
        try:
            sent_count = send_mail(
                subject=title,
                message=message,
                from_email=from_email,
                recipient_list=[email_address],
                fail_silently=False,
            )
            return sent_count > 0
        except Exception as exc:
            logger.error(
                f"Failed to send email to {email_address} with title '{title}': {exc}"
            )
            return False


class SMSBackend(BaseNotificationBackend):
    """
    SMS delivery backend tailored for the Nigerian telecommunications environment.

    Default Integration: Termii API (https://termii.com)
    - Termii is the standard SMS & OTP gateway in Nigeria for DND-compliant routing.
    - Endpoint: https://api.ng.termii.com/api/sms/send
    - Requires: TERMII_API_KEY, TERMII_SENDER_ID in settings / env.
    - Phone number formatting: expects international format with Nigerian prefix +234
    """

    TERMII_BASE_URL = "https://api.ng.termii.com/api/sms/send"

    def __init__(self, api_key=None, sender_id=None):
        self.api_key = api_key or getattr(settings, "TERMII_API_KEY", "")
        self.sender_id = sender_id or getattr(settings, "TERMII_SENDER_ID", "SchoolMS")

    def format_phone_number(self, phone):
        """Format Nigerian phone numbers into 234XXXXXXXXXX international format."""
        if not phone:
            return None
        cleaned = "".join(filter(str.isdigit, phone))
        if cleaned.startswith("0") and len(cleaned) == 11:
            return "234" + cleaned[1:]
        elif cleaned.startswith("234") and len(cleaned) == 13:
            return cleaned
        return cleaned

    def send(self, recipient, title, message, **kwargs):
        phone_number = getattr(recipient, "phone_number", None)
        if not phone_number:
            logger.warning(
                f"Cannot send SMS: recipient {recipient} has no phone_number attribute."
            )
            return False

        formatted_phone = self.format_phone_number(phone_number)
        if not formatted_phone:
            logger.warning(f"Invalid phone number '{phone_number}' for recipient {recipient}.")
            return False

        # If API key is not configured (e.g. development/testing), log and succeed
        if not self.api_key:
            logger.info(
                f"[MOCK SMS] To: {formatted_phone} | Sender: {self.sender_id} | Message: {title}: {message}"
            )
            return True

        payload = {
            "to": formatted_phone,
            "from": self.sender_id,
            "sms": f"{title}\n{message}",
            "type": "plain",
            "channel": "generic",  # or 'dnd' for priority transactional route
            "api_key": self.api_key,
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            http_req = request.Request(
                self.TERMII_BASE_URL,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with request.urlopen(http_req, timeout=10) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                if resp_data.get("code") == "ok" or resp.status in (200, 201):
                    logger.info(f"SMS successfully sent to {formatted_phone}")
                    return True
                else:
                    logger.warning(f"Termii returned non-ok status: {resp_data}")
                    return False
        except error.HTTPError as exc:
            logger.error(f"Termii HTTP error {exc.code}: {exc.read().decode('utf-8')}")
            return False
        except Exception as exc:
            logger.error(f"Failed to dispatch SMS to {formatted_phone}: {exc}")
            return False


def get_notification_backend(channel):
    """Backend factory helper."""
    backends = {
        "in_app": InAppBackend,
        "email": EmailBackend,
        "sms": SMSBackend,
    }
    backend_class = backends.get(channel)
    if not backend_class:
        raise ValueError(f"Unknown notification channel: {channel}")
    return backend_class()
