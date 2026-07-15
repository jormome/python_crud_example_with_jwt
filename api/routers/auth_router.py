"""
Auth router for authentication endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies.user_dependency import get_user_service
from api.schemas.auth_dto import LoginRequestDto, LoginResponseDto
from api.services.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/token", response_model=LoginResponseDto)
async def login(
    data: LoginRequestDto,
    service: Annotated[UserService, Depends(get_user_service)],
) -> LoginResponseDto:
    return service.login(data)


@auth_router.post("/token/form", response_model=LoginResponseDto)
def login_form(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
) -> LoginResponseDto:
    """Acepta credenciales desde un formulario y devuelve un token JWT."""
    return service.login(
        LoginRequestDto(
            email=form.username,
            password=form.password,
        )
    )
