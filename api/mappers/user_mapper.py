"""Conversores entre entidades SQLAlchemy y DTOs Pydantic."""

from api.entities.user import User
from api.schemas.user_dto import UserCreateDto, UserResponseDto


class UserMapper:
    """Centraliza la transformación entre modelos internos y respuestas externas."""

    @staticmethod
    def to_response_dto(entity: User) -> UserResponseDto:
        """Convierte una entidad User en un DTO de respuesta."""
        return UserResponseDto.model_validate(entity)

    @staticmethod
    def to_entity(dto: UserCreateDto) -> User:
        """Convierte un DTO de creación en una entidad User."""
        return User(
            email=dto.email,
            password=dto.password,
            is_active=dto.is_active,
        )
