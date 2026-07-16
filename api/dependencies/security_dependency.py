"""
Secure dependency for authenticated users.
"""

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from api.dependencies.user_dependency import get_user_service
from api.entities.user import User
from api.schemas.user_dto import UserResponseDto
from api.services.jwt_service import JwtService
from api.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token/form")


def get_authenticated_user(
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> UserResponseDto:
    """
    Obtains the authenticated user from the token.

    Args:
        service: UserService instance
        token: JWT token

    Returns:
        UserResponseDto: Authenticated user
    """

    user_id: int = JwtService.verify_token(token)
    user: User = service.find_by_id(user_id)

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive",
        )

    return user
