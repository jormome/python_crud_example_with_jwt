import logging

from fastapi import HTTPException

from api.entities.user import User
from api.exceptions.exceptions import AuthenticationException, NotFoundException
from api.repositories.user_repository import UserRepository
from api.schemas.auth_dto import LoginRequestDto, LoginResponseDto
from api.schemas.user_dto import UserUpdateDto
from api.security.passwords_security import PasswordSecurity
from api.services.generic_service import GenericService
from api.services.jwt_service import JwtService

logger: logging.Logger = logging.getLogger(__name__)


class UserService(
    GenericService[
        User,
        int,
    ]
):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.user_repository: UserRepository = repository

    def get_by_email(self, email: str) -> User:
        """
        Find a user by email.

        Args:
            email: The email of the user to find

        Returns:
            User: The user with the given email
        """
        user = self.user_repository.find_by_email(email)
        if user is None:
            logger.warning(f"User with email {email} not found")
            raise NotFoundException("User not found")
        return user

    def update(self, entity_id: int, user: UserUpdateDto) -> User:
        """
        Update a user.

        Args:
            entity_id: The ID of the user to update
            user: The user with the changes to apply

        Returns:
            User: The updated user
        """
        changes = user.model_dump(exclude_unset=True)
        if "password" in changes:
            changes["password"] = PasswordSecurity.hash_password(changes["password"])
        return self._apply_changes(entity_id, changes)

    def authenticate(self, email: str, password: str) -> User:
        """
        Authenticate a user.

        Args:
            email: The email of the user to authenticate
            password: The password of the user to authenticate

        Returns:
            User: The authenticated user
        """
        user: User | None = self.user_repository.find_by_email(email)

        if user is None:
            logger.warning(f"User with email {email} not found")
            # raise HTTPException(status_code=401, detail="Incorrect email or password")
            # con esta excepcion personalizada queda mas desacoplado de FastAPI
            raise AuthenticationException("Incorrect email or password")

        if not PasswordSecurity.verify_password(password, user.password):
            logger.warning(f"Invalid password for user with email {email}")
            raise AuthenticationException("Incorrect email or password")

        return user

    # Aquí sí acepto DTO. Porque login es un caso de uso. No un CRUD.
    def login(self, dto: LoginRequestDto) -> LoginResponseDto:
        """Authenticate a user and generate an access token.

        Args:
            dto: Login credentials provided by the client.

        Returns:
            A response DTO containing the generated JWT.

        Raises:
            HTTPException: If the credentials are invalid or the user is inactive.
        """
        user: User = self.authenticate(dto.email, dto.password)

        if not user.is_active:
            logger.warning(f"User with email {dto.email} is inactive")
            raise HTTPException(status_code=401, detail="Inactive user")

        token: str = JwtService.create_token(user)
        return LoginResponseDto(access_token=token)
