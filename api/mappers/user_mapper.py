"""Conversores entre entidades SQLAlchemy y DTOs Pydantic."""

from api.entities.user import User
from api.schemas.user_dto import UserCreateDto, UserResponseDto, UserUpdateDto
from api.security.passwords_security import PasswordSecurity


class UserMapper:
    """Centraliza la transformación entre modelos internos y respuestas externas."""

    @staticmethod
    def to_response_dto(
        entity: User,
    ) -> UserResponseDto:
        """Convierte una entidad User en un DTO de respuesta."""

        return UserResponseDto.model_validate(entity)

    @staticmethod
    def to_entity(
        user: UserCreateDto | UserUpdateDto,
    ) -> User:
        password: str | None = (
            PasswordSecurity.hash_password(user.password) if user.password else None
        )
        return User(
            email=user.email,
            password=password,
            is_active=user.is_active,
        )
