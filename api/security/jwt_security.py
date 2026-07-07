"""Utilidades de seguridad para generar y validar tokens JWT."""

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException
from jose import JWTError, jwt

from api.config.settings import settings
from api.schemas.user_dto import UserResponseDto


class JwtService:
    """Proporciona operaciones de emisión y verificación de tokens JWT."""

    @staticmethod
    def create_access_token(user: UserResponseDto) -> str:
        """Crea un JWT con la identidad del usuario y su tiempo de expiración."""
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
        """Valida un token y devuelve el identificador del usuario."""
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
