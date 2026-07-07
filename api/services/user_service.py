"""Business logic for user management and authentication.

This module contains the service layer that coordinates repository access,
password hashing, transactional persistence, and JWT-based authentication
for application users.
"""

import logging
import logging.config
from collections.abc import Generator
from contextlib import contextmanager

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.config.logging_config import LOGGING_CONFIG
from api.entities.user import User
from api.exceptions.exceptions import ConflictError, NotFoundError
from api.mappers.user_mapper import UserMapper
from api.repositories.user_repository import UserRepository
from api.schemas.auth_dto import LoginRequestDto, LoginResponseDto
from api.schemas.user_dto import UserCreateDto, UserResponseDto
from api.security.passwords_security import PasswordHasher
from api.services.generic_service import GenericService
from api.services.jwt_service import JwtService

logging.config.dictConfig(LOGGING_CONFIG)
logger: logging.Logger = logging.getLogger(__name__)


class UserService(GenericService[User, UserCreateDto, UserResponseDto, int]):
    """Service responsible for user CRUD operations and authentication."""

    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service with a user repository.

        Args:
            repository: Repository instance used to query and persist users.
        """
        super().__init__()
        self._repository: UserRepository = repository
        self._db: Session = repository.db

    @contextmanager
    def _transaction(self) -> Generator[None, None, None]:
        """Wrap repository operations in a transactional context.

        The context commits changes on success and rolls back on failure,
        ensuring that data writes remain consistent.
        """
        try:
            yield
            self._db.commit()
            logger.debug("Transaction committed")

        except Exception as exc:
            self._db.rollback()
            logger.error(f"Transaction rolled back due to: {exc}")
            raise

    def find_all(self) -> list[UserResponseDto]:
        """Return all users as response DTOs."""
        return [
            UserMapper.to_response_dto(entity) for entity in self._repository.find_all()
        ]

    def find_by_id(self, entity_id: int) -> UserResponseDto | None:
        """Return a user by its identifier, if it exists."""
        entity: User | None = self._repository.find_by_id(entity_id)
        return UserMapper.to_response_dto(entity) if entity else None

    def find_by_email(self, email: str) -> UserResponseDto | None:
        """Return a user by email, if it exists."""
        entity: User | None = self._repository.find_by_email(email)
        return UserMapper.to_response_dto(entity) if entity else None

    def create(self, dto: UserCreateDto) -> UserResponseDto:
        """Create a new user after validating that the email is available.

        Args:
            dto: Data transfer object containing the new user information.

        Returns:
            The created user represented as a response DTO.

        Raises:
            ConflictError: If the provided email is already registered.
        """
        if self._repository.find_by_email(dto.email):
            raise ConflictError("Email already exists")

        with self._transaction():
            new_user = User(**dto.model_dump())
            new_user.password = PasswordHasher.hash_password(new_user.password)
            self._repository.add(new_user)

        logger.info(f"Created user with id {new_user.id}")
        return UserMapper.to_response_dto(new_user)

    def update(self, entity_id: int, dto: UserCreateDto) -> UserResponseDto:
        """Update an existing user with the provided values.

        Args:
            entity_id: Identifier of the user to update.
            dto: New values for the user.

        Returns:
            The updated user as a response DTO.

        Raises:
            NotFoundError: If the user does not exist.
        """
        existing: User | None = self._repository.find_by_id(entity_id)
        if not existing:
            raise NotFoundError(f"User {entity_id} not found")

        with self._transaction():
            for key, value in dto.model_dump(exclude_unset=True).items():
                if key != "id":
                    setattr(existing, key, value)

        self._db.refresh(existing)
        logger.info(f"Updated user {entity_id}")
        return UserMapper.to_response_dto(existing)

    def delete(self, entity_id: int) -> None:
        """Delete a user by identifier.

        Args:
            entity_id: Identifier of the user to delete.

        Raises:
            NotFoundError: If the user does not exist.
        """
        existing: User | None = self._repository.find_by_id(entity_id)
        if not existing:
            raise NotFoundError(f"User {entity_id} not found")

        with self._transaction():
            self._repository.delete(existing)

        logger.info(f"Deleted user {entity_id}")

    def authenticate(self, email: str, password: str) -> UserResponseDto | None:
        """Validate credentials and return a user if authentication succeeds."""
        user: User | None = self._repository.find_by_email(email)
        if not user:
            return None

        if not PasswordHasher.verify_password(password, user.password):
            return None

        return UserMapper.to_response_dto(user) if user.is_active else None

    def login(self, dto: LoginRequestDto) -> LoginResponseDto:
        """Authenticate a user and generate an access token.

        Args:
            dto: Login credentials provided by the client.

        Returns:
            A response DTO containing the generated JWT.

        Raises:
            HTTPException: If the credentials are invalid or the user is inactive.
        """
        user: UserResponseDto | None = self.authenticate(dto.email, dto.password)
        if not user:
            logger.warning(f"Login failed for {dto.email}")
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        if not user.is_active:
            raise HTTPException(status_code=401, detail="Inactive user")

        token: str = JwtService.create_access_token(user)
        return LoginResponseDto(access_token=token)
