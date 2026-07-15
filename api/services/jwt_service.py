"""
Service for JWT operations (create and validate).
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException
from jose import jwt

from api.config.settings import settings
from api.schemas.user_dto import UserResponseDto


class JwtService:
    """
    Service for JWT operations.
    """

    @staticmethod
    def create_token(user: UserResponseDto) -> str:
        """
        Create the JWT token for user.
        """
        expire: datetime = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload: dict[str, Any] = {
            "sub": str(user.id),
            "email": user.email,
            "iat": datetime.now(UTC),
            "exp": expire,
        }
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def verify_token(token: str) -> int:
        """
        Verify the JWT token.
        """
        try:
            payload: dict[str, Any] = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Token inválido")
            return int(user_id)

        except Exception as e:
            print(repr(e))
            raise
