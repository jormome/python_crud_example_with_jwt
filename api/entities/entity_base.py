"""Modelo base compartido por todas las entidades SQLAlchemy de la API."""

from sqlalchemy.orm import Mapped, mapped_column

from api.config.db import Base


class EntityBase(Base):
    """Clase base abstracta con el identificador común para todas las entidades."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
