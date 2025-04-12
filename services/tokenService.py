from typing import Any

from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer

from config import settings
from models.user import User
from repositories.userRepository import userRepository
from utils.types import TokenPayload


class TokenService:
    @staticmethod
    def generate(payload: dict[str, Any]) -> str:
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        token = serializer.dumps(payload, salt=app.config["SECURITY_PASSWORD_SALT"])
        return token

    @staticmethod
    def getPayload(token: str) -> TokenPayload | None:
        try:
            serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
            payload = serializer.loads(
                token,
                salt=app.config["SECURITY_PASSWORD_SALT"],
                max_age=settings.API_TOKEN_EXPIRES,
            )
            return payload
        except Exception:
            return None

    @classmethod
    def verify(cls, token: str) -> User | None:
        try:
            payload = cls.getPayload(token)
            if not payload:
                raise Exception
            user = userRepository.getByPublicId(payload["publicId"])
            if payload["isActive"] == user.isActive:
                return user
        except Exception:
            return None
