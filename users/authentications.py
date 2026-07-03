import logging

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

from users import defaults

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get(defaults.ACCESS_TOKEN_COOKIE_KEY_NAME, None)
        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            self.enforce_csrf(request)
            return user, validated_token
        except (TokenError, InvalidToken):
            return None

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for cookie based authentication.
        """
        check = CSRFCheck(get_response=lambda req: None)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')
