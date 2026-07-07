"""Entidad de usuario persistida en la base de datos."""

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.entities.entity_base import EntityBase


class User(EntityBase):
    """Representa a un usuario autenticable dentro del sistema."""

    __tablename__: str = "users"

    email: Mapped[EmailStr] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
