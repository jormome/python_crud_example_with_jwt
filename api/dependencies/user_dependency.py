"""
User dependency for database operations.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from api.config.db import SessionLocal
from api.repositories.user_repository import UserRepository
from api.services.user_service import UserService


def get_db():
    """
    Dependecy to get a database session.
    """

    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


def get_user_repository(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
) -> UserRepository:
    """
    Creates a user repository for each request.
    """
    return UserRepository(session=session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """
    Creates a user service for each request.
    """
    return UserService(repository=repository)
