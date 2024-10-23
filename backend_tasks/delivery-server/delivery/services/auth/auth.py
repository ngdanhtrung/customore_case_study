import jwt
from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.decorators import api_view

from delivery.utils.validation import ValidationError, ValidationCodeEnum

from delivery.configs.settings import (
    ACCESS_TOKEN_EXPIRE_TIME,
    REFRESH_ACCESS_TOKEN_EXPIRE_TIME,
    ACCESS_TOKEN_SECRET,
    REFRESH_TOKEN_SECRET,
)


def generate_refresh_token(username: str):
    serviceID = "delivery"

    created_at = datetime.now()
    expire_at = datetime.now() + timedelta(minutes=REFRESH_ACCESS_TOKEN_EXPIRE_TIME)

    payload = {
        "iss": serviceID,
        "sub": username,
        "iat": int(created_at.timestamp()),
        "exp": int(expire_at.timestamp()),
        "aud": ["delivery"],
    }

    token = jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm="HS256")
    return token


def generate_token(username: str, user_id: int, role: str = "user"):
    serviceID = "delivery"

    created_at = datetime.now()
    expire_at = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)

    payload = {
        "iss": serviceID,
        "sub": username,
        "user_id": user_id,
        "role": role,
        "iat": int(created_at.timestamp()),
        "exp": int(expire_at.timestamp()),
        "aud": ["delivery"],
    }

    token = jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm="HS256")
    return token
