"""
User entity
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.entities.entity_base import EntityBase


class User(EntityBase):
    """
    User entity for the database
    """

    __tablename__: str = "users"

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
