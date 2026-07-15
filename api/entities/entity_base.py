"""
Base class for all entities
"""

from sqlalchemy.orm import Mapped, mapped_column

from api.config.db import Base


class EntityBase(Base):
    """Base class for all entities that have an ID of type int"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
