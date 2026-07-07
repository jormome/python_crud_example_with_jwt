"""Helpers for creating and validating JWT-based access tokens."""

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException
from jose import JWTError, jwt

from api.config.settings import settings
from api.schemas.user_dto import UserResponseDto


class JwtService:
    """Utility service for issuing and validating JWT access tokens."""

    @staticmethod
    def create_access_token(user: UserResponseDto) -> str:
        """Create a signed JWT for an authenticated user.

        Args:
            user: The authenticated user whose identity will be encoded.

        Returns:
            A compact JWT string that can be used as an access token.
        """
        expire: datetime = datetime.now(UTC) + timedelta(
            minutes=settings.JWT_EXP_MINUTES
        )
        payload: dict[str, Any] = {
            "sub": str(user.id),
            "email": user.email,
            "iat": datetime.now(UTC),
            "exp": expire,
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> int:
        """Decode and validate a JWT token, returning the user identifier.

        Args:
            token: The JWT string received from the client.

        Returns:
            The user identifier stored in the token payload.

        Raises:
            HTTPException: If the token is missing, malformed, or invalid.
        """
        try:
            payload: dict[str, Any] = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: Any | None = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return int(user_id)
        except JWTError as exc:
            raise HTTPException(status_code=401, detail="Invalid token") from exc
