import secrets
import string
from rest_framework.response import Response
import random

from users.defaults import (
    ACCESS_TOKEN_COOKIE_KEY_NAME,
    REFRESH_TOKEN_COOKIE_KEY_NAME,
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
)


def set_cookie(response: Response, key, value, max_age=REFRESH_TOKEN_LIFETIME * 86400):
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        httponly=True,
        samesite='None',
        secure=True,
    )


def set_tokens_on_cookie(response: Response, access_token: str, refresh_token: str):
    set_cookie(response, ACCESS_TOKEN_COOKIE_KEY_NAME, access_token, ACCESS_TOKEN_LIFETIME)
    set_cookie(response, REFRESH_TOKEN_COOKIE_KEY_NAME, refresh_token)


def remove_tokens_from_cookie(response: Response):
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE_KEY_NAME,
        samesite='None',
        secure=True,
    )
    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY_NAME,
        samesite='None',
        secure=True,
    )


def generate_random_password(length=25):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def generate_otp(length=4):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])