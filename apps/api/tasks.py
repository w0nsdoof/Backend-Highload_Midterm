from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_order_confirmation_email(order_id, user_email):
    try:
        subject = "Order Confirmation"
        message = f"Your order with ID {order_id} has been successfully placed."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {str(e)}")
        raise e
