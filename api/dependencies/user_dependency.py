"""Dependencias para construir los repositorios y servicios de usuario."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from api.config.db import get_db
from api.repositories.user_repository import UserRepository
from api.services.user_service import UserService


def get_user_repository(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> UserRepository:
    """Crea un repositorio de usuarios para cada solicitud."""
    return UserRepository(session)


def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> UserService:
    """Crea el servicio de usuarios a partir del repositorio inyectado."""
    return UserService(repository=repository)
