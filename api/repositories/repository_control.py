"""
Repository protocol for database operations.
"""

from typing import Protocol, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")
ID = TypeVar(
    "ID",
    contravariant=True,
)


class RepositoryProtocol(Protocol[T, ID]):
    """
    Repository protocol for database operations.
    """

    session: Session

    def find_all(self) -> list[T]: ...
    def find_by_id(self, id: ID) -> T | None: ...
    def add(self, entity: T) -> T: ...
    def delete(self, entity_id: ID) -> None: ...
