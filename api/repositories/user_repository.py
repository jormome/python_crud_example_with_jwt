"""Repositorio específico para operaciones relacionadas con usuarios."""

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from api.entities.user import User
from api.repositories.generic_repository import GenericRepository


class UserRepository(GenericRepository[User, int]):
    """Extiende el repositorio base con consultas específicas de usuario."""

    def __init__(self, db: Session) -> None:
        """Inicializa el repositorio con la entidad User."""
        super().__init__(db, User)

    def find_by_email(self, email: str) -> User | None:
        """Busca un usuario por su dirección de correo electrónico."""
        sql: Select[tuple[User]] = select(User).where(User.email == email)
        return self.db.scalar(sql)
