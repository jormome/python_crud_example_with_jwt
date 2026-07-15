import logging
from abc import ABC
from contextlib import contextmanager
from typing import Any, Generator, Generic, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.entities.entity_base import EntityBase
from api.exceptions.exceptions import NotFoundException
from api.repositories.repository_control import RepositoryProtocol

T = TypeVar("T", bound=EntityBase)
ID = TypeVar("ID")


logger: logging.Logger = logging.getLogger(__name__)


class GenericService(ABC, Generic[T, ID]):
    """Service responsible for user CRUD operations and authentication."""

    def __init__(self, repository: RepositoryProtocol[T, ID]):
        """
        Initialize the service with a repository.

        Args:
            repository: The repository to use for database operations
        """
        self.repository: RepositoryProtocol[T, ID] = repository
        self._session: Session = repository.session

    @contextmanager
    def _transaction(self) -> Generator[None, None, None]:
        """
        Context manager for database transactions.

        Yields:
            None
        """
        try:
            yield
            self._session.commit()
            logger.info("Transaction committed")

        except SQLAlchemyError as e:
            self._session.rollback()
            logger.error(f"Transaction failed and rolled back: {e}", exc_info=True)
            raise

        except Exception as e:
            self._session.rollback()
            logger.error(f"Unexpected error inside transaction: {e}", exc_info=True)
            raise

    def find_all(self) -> list[T]:
        """
        Get all entities.

        Returns:
            list[DTO]: List of all entities
        """
        return self.repository.find_all()

    def find_by_id(
        self,
        id: ID,
    ) -> T:  # devuelvo siempre T porque si es None lanzo un error
        """
        Find an entity by ID.

        Args:
            id: The ID of the entity to find

        Returns:
            DTO | None: The entity with the given ID, or None if not found
        """

        entity: T | None = self.repository.find_by_id(id)
        if entity is None:
            logger.warning(f"Entity with ID {id} not found")
            raise NotFoundException("Entity not found")
        return entity

    def create(self, entity: T) -> T:
        """
        Save an entity.

        Args:
            entity: The entity to save

        Returns:
            DTO: The saved entity
        """
        with self._transaction():
            return self.repository.add(entity)

    def _apply_changes(
        self,
        entity_id: ID,
        changes: dict[str, Any],
    ) -> T:
        """
        Update an entity.

        Args:
            entity_id: The ID of the entity to update
            update_dto: The update data (all fields optional)

        Returns:
            T: The updated entity

        Raises:
            NotFoundException: If user doesn't exist
            ConflictException: If email already exists for another user
        """

        with self._transaction():
            # find_by_id already raises NotFoundException if entity not found
            entity: T = self.find_by_id(entity_id)

            for field, value in changes.items():
                setattr(entity, field, value)

            return self.repository.add(entity)

    def delete(self, entity_id: ID) -> None:
        """
        Delete an entity.

        Args:
            entity_id: The ID of the entity to delete
        """
        with self._transaction():
            self.repository.delete(entity_id)
