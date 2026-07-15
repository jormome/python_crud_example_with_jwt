"""
User router for user management endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from api.dependencies.security_dependency import get_authenticated_user
from api.dependencies.user_dependency import get_user_service
from api.entities.user import User
from api.exceptions.exceptions import AuthorizationException
from api.mappers.user_mapper import UserMapper
from api.schemas.user_dto import UserCreateDto, UserResponseDto, UserUpdateDto
from api.services.user_service import UserService

user_router = APIRouter()


@user_router.get("/", response_model=list[UserResponseDto])
def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    _: Annotated[UserResponseDto, Depends(get_authenticated_user)],
) -> list[UserResponseDto]:
    """Devuelve la lista completa de usuarios."""
    users = service.find_all()
    return [UserMapper.to_response_dto(user) for user in users]


@user_router.get("/{user_id}", response_model=UserResponseDto)
def list_by_id(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
    authenticated_user: Annotated[UserResponseDto, Depends(get_authenticated_user)],
) -> UserResponseDto:
    """Devuelve un usuario específico si coincide con el usuario autenticado."""
    if user_id != authenticated_user.id:
        raise AuthorizationException()

    user: User = service.find_by_id(user_id)
    return UserMapper.to_response_dto(user)


@user_router.post("/", response_model=UserResponseDto, status_code=201)
def create(
    service: Annotated[UserService, Depends(get_user_service)],
    user: UserCreateDto,
) -> UserResponseDto:
    """Crea un nuevo usuario en el sistema."""
    return service.create(UserMapper.to_entity(user))


@user_router.put("/{user_id}", response_model=UserResponseDto)
def update(
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
    user: UserUpdateDto,
    authenticated_user: Annotated[UserResponseDto, Depends(get_authenticated_user)],
) -> UserResponseDto:
    """Actualiza los datos de un usuario autenticado."""
    if user_id != authenticated_user.id:
        raise AuthorizationException()

    update = service.update(user_id, user)
    return UserMapper.to_response_dto(update)


@user_router.delete("/{user_id}", status_code=204)
def delete(
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
    authenticated_user: Annotated[UserResponseDto, Depends(get_authenticated_user)],
) -> Response:
    """Elimina un usuario autenticado del sistema."""
    if user_id != authenticated_user.id:
        raise AuthorizationException()

    service.delete(user_id)
    return Response(status_code=204)
