import random
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from users.defaults import OTP_EXPIRY_SECONDS
from users.tasks import send_otp_sms

User = get_user_model()

class OTPService:
    @staticmethod
    def generate_otp(length=4) -> str:
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def request_otp(phone_number: str) -> None:
        """
        Generates and sends an OTP via SMS to the specified phone number.
        """
        # A proper throttling is enforced at the View layer via DRF Throttling.
        # But we could also check cache directly if we want a hard lock.
        otp = OTPService.generate_otp()
        cache.set(f"otp_{phone_number}", otp, timeout=OTP_EXPIRY_SECONDS)
        send_otp_sms.delay(phone_number, otp)

    @staticmethod
    def verify_otp(phone_number: str, incoming_otp: str) -> bool:
        """
        Verifies the incoming OTP for the given phone number.
        Returns True if valid, False otherwise.
        """
        cached_otp = cache.get(f"otp_{phone_number}")
        if not cached_otp or str(cached_otp) != str(incoming_otp):
            return False
        
        # Valid OTP, consume it
        cache.delete(f"otp_{phone_number}")
        return True


class UserService:
    @staticmethod
    def create_user(phone_number: str, password: str = None) -> User:
        """
        Creates a new user.
        """
        return User.objects.create_user(phone_number=phone_number, password=password)

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        """
        Generates access and refresh tokens for a user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def mark_phone_as_verified(user: User) -> None:
        """
        Marks a user's phone number as verified.
        """
        if not user.is_phone_verified:
            user.is_phone_verified = True
            user.save(update_fields=("is_phone_verified", "updated_at"))
