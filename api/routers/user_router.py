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


@user_router.get(
    "/",
    response_model=list[UserResponseDto],
)
def list_users(
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    _: Annotated[
        UserResponseDto,
        Depends(get_authenticated_user),
    ],
) -> list[UserResponseDto]:
    """Returns the list of all users.

    Args:
        service: The user service
        authenticated_user: The authenticated user

    Returns:
        list[UserResponseDto]: The list of users
    """

    users: list[User] = service.find_all()
    return [UserMapper.to_response_dto(user) for user in users]


@user_router.get(
    "/{user_id}",
    response_model=UserResponseDto,
)
def list_by_id(
    user_id: int,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    authenticated_user: Annotated[
        UserResponseDto,
        Depends(get_authenticated_user),
    ],
) -> UserResponseDto:
    """Returns a specific user if it matches the authenticated user.

    Args:
        user_id: The user id
        service: The user service
        authenticated_user: The authenticated user

    Returns:
        UserResponseDto: The user
    """

    if user_id != authenticated_user.id:
        raise AuthorizationException()

    user: User = service.find_by_id(user_id)
    return UserMapper.to_response_dto(user)


@user_router.post(
    "/",
    response_model=UserResponseDto,
    status_code=201,
)
def create(
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    user: UserCreateDto,
) -> UserResponseDto:
    """Creates a new user in the system.

    Args:
        service: The user service
        user: The user to create

    Returns:
        UserResponseDto: The created user
    """

    return service.create(UserMapper.to_entity(user))


@user_router.put(
    "/{user_id}",
    response_model=UserResponseDto,
)
def update(
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    user_id: int,
    user: UserUpdateDto,
    authenticated_user: Annotated[
        UserResponseDto,
        Depends(get_authenticated_user),
    ],
) -> UserResponseDto:
    """Updates the data of an authenticated user.

    Args:
        service: The user service
        user_id: The user id
        user: The user to update
        authenticated_user: The authenticated user

    Returns:
        UserResponseDto: The updated user
    """

    if user_id != authenticated_user.id:
        raise AuthorizationException()

    update: User = service.update(user_id, user)
    return UserMapper.to_response_dto(update)


@user_router.delete(
    "/{user_id}",
    status_code=204,
)
def delete(
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    user_id: int,
    authenticated_user: Annotated[
        UserResponseDto,
        Depends(get_authenticated_user),
    ],
) -> Response:
    """Deletes an authenticated user from the system.

    Args:
        service: The user service
        user_id: The user id
        authenticated_user: The authenticated user

    Returns:
        Response: The response
    """

    if user_id != authenticated_user.id:
        raise AuthorizationException()

    service.delete(user_id)
    return Response(status_code=204)
