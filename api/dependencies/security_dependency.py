"""Dependencias de seguridad para autenticar usuarios mediante JWT."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.dependencies.user_dependency import get_user_service
from api.schemas.user_dto import UserResponseDto
from api.services.jwt_service import JwtService
from api.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token/form")


def get_authenticated_user(
    service: Annotated[UserService, Depends(get_user_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponseDto:
    """Valida un token JWT y devuelve el usuario autenticado."""
    user_id: int = JwtService.decode_token(token)
    user: UserResponseDto | None = service.find_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or inactive user"
        )
    return user
