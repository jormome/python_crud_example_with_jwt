from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.entities.entity_base import EntityBase

T = TypeVar("T", bound=EntityBase)
ID = TypeVar("ID")


class GenericRepository(Generic[T, ID]):
    """Repository responsible for user CRUD operations and authentication."""

    def __init__(self, session: Session, model: type[T]) -> None:
        """
        Initialize the repository with a session and model.

        Args:
            session: The database session to use
            model: The model to use
        """
        self.session: Session = session
        self.model: type[T] = model

    def find_all(self) -> list[T]:
        """
        Find all entities.

        Returns:
            list[T]: List of all entities
        """
        sql = select(self.model).order_by(self.model.id.asc())
        return list(self.session.execute(sql).scalars().all())

    def find_by_id(self, id: ID) -> T | None:
        """
        Find an entity by its ID.

        Args:
            id: The ID of the entity to find

        Returns:
            T | None: The entity with the given ID, or None if not found
        """
        sql = select(self.model).where(self.model.id == id)
        return self.session.execute(sql).scalars().first()

    def add(self, entity: T) -> T:
        """
        Save an entity.

        Args:
            entity: The entity to save

        Returns:
            T: The saved entity
        """
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def delete(self, entity_id: ID) -> None:
        """
        Delete an entity.

        Args:
            entity: The entity to delete
        """
        entity = self.find_by_id(entity_id)
        if entity is None:
            raise ValueError(f"Entity with id {entity_id} not found")
        self.session.delete(entity)

    def exists(self, entity_id: ID) -> bool:
        """
        Check if an entity exists.

        Args:
            entity_id: The ID of the entity to check

        Returns:
            bool: True if the entity exists, False otherwise
        """
        return self.find_by_id(entity_id) is not None
