from typing import Tuple

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from api.entities.user import User
from api.repositories.generic_repository import GenericRepository


class UserRepository(GenericRepository[User, int]):
    """
    Repository for user-related database operations.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Initialize the user repository.

        Args:
            session: The database session to use
        """

        super().__init__(session, User)

    def find_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Find a user by email.

        Args:
            email: The email of the user to find

        Returns:
            User | None: The user with the given email, or None if not found
        """

        sql: Select[Tuple[User]] = select(User).where(User.email == email)
        return self.session.execute(sql).scalars().first()
