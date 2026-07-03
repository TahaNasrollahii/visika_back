import requests
import os
from django.conf import settings
from rest_framework.exceptions import APIException


class SMSProviderException(APIException):
    status_code = 502
    default_detail = "SMS Provider failed to process the request."
    default_code = "sms_provider_error"


class SMSHandler:
    BASE_URL = "https://edge.ippanel.com/v1"
    
    def __init__(self):
        self.api_key = getattr(settings, "FARAZ_SMS_API_KEY", "")
        self.sender_number = getattr(settings, "FARAZ_SMS_SENDER_NUMBER", "")
        self.login_otp_pattern_code = getattr(settings, "FARAZ_SMS_LOGIN_OTP_PATTERN_CODE", "")
        self.validate_env_config() 
            
    def validate_env_config(self):
        required_fields = ("api_key", "sender_number", "login_otp_pattern_code")
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Faraz sms {field} is not properly set in settings.")
    
    def get_headers(self):
        return {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        
    def send_request(self, method, url, headers, body):
        try:
            response = requests.request(
                url=url,
                method=method,
                headers=headers,
                json=body,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Re-raise as custom exception to allow celery to retry
            raise SMSProviderException(f"Failed to communicate with SMS provider: {e}")
    
    def send_sms_with_pattern(self, recipient_phone_number, otp_code):
        url = f"{self.BASE_URL}/api/send"
        headers = self.get_headers()
        body = {
            "sending_type": "pattern",
            "from_number": self.sender_number,
            "code": self.login_otp_pattern_code,
            "recipients": [recipient_phone_number],
            "params": {"verification-code": otp_code,},
        }
        return self.send_request(
            method="POST",
            url=url,
            headers=headers,
            body=body,
        )