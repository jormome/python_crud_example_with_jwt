"""Repositorio genérico para operaciones CRUD sobre entidades SQLAlchemy."""

from typing import Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from api.entities.entity_base import EntityBase

T = TypeVar("T", bound=EntityBase)
ID = TypeVar("ID")


class GenericRepository(Generic[T, ID]):
    """Proporciona operaciones básicas reutilizables para cualquier entidad."""

    def __init__(
        self,
        db: Session,
        entity: type[T],
    ) -> None:
        """Inicializa el repositorio con la sesión y la entidad objetivo."""
        self.db: Session = db
        self._entity: type[T] = entity

    def find_all(self) -> list[T]:
        """Devuelve todos los registros de la entidad, ordenados por identificador."""
        sql: Select[tuple[T]] = select(self._entity).order_by(self._entity.id.asc())
        return list(self.db.scalars(sql).all())

    def find_by_id(self, entity_id: ID) -> T | None:
        """Busca una entidad por su clave primaria."""
        return self.db.get(self._entity, entity_id)

    def add(self, entity: T) -> T:
        """Registra una nueva entidad para su posterior persistencia."""
        self.db.add(entity)
        return entity

    def delete(self, entity: T) -> None:
        """Marca una entidad existente para ser eliminada."""
        self.db.delete(entity)
