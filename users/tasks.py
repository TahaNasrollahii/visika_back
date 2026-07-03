from celery import shared_task
import logging
from third_parties.sms.faraz_sms import SMSHandler, SMSProviderException

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_otp_sms(self, phone_number, otp_code):
    try:
        sms_handler = SMSHandler()
        sms_handler.send_sms_with_pattern(
            recipient_phone_number=phone_number, 
            otp_code=otp_code
        )
    except SMSProviderException as e:
        logger.warning(f"SMSProviderException: {e}. Retrying...")
        raise self.retry(exc=e)
    except Exception as e:
        logger.error(f"Failed to send SMS due to an unexpected error: {e}", exc_info=True)
        # We don't retry on unexpected exceptions (like configuration errors)
        raise