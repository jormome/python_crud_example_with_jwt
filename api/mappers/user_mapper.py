"""
User mapper for mapping between entities and DTOs
"""

from api.entities.user import User
from api.schemas.user_dto import UserCreateDto, UserResponseDto, UserUpdateDto
from api.security.passwords_security import PasswordSecurity


class UserMapper:
    """
    User mapper for mapping between entities and DTOs
    """

    @staticmethod
    def to_response_dto(
        entity: User,
    ) -> UserResponseDto:
        """
        Convert a User entity to a UserResponseDto

        Args:
            user: User entity

        Returns:
            UserResponseDto
        """

        return UserResponseDto.model_validate(entity)

    @staticmethod
    def to_entity(
        user: UserCreateDto | UserUpdateDto,
    ) -> User:
        """
        Convert a UserCreateDto or UserUpdateDto to a User entity

        Args:
            user: UserCreateDto or UserUpdateDto

        Returns:
            User entity
        """

        password: str | None = (
            PasswordSecurity.hash_password(user.password) if user.password else None
        )
        return User(
            email=user.email,
            password=password,
            is_active=user.is_active,
        )
