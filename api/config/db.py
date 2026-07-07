"""Configuración central de la base de datos para la aplicación."""

from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from api.config.settings import settings

if not settings.DATABASE_URI:
    raise ValueError("DATABASE_URI no está configurada en las variables de entorno.")

engine: Engine = create_engine(
    settings.DATABASE_URI,
    echo=True,
    pool_size=20,
    max_overflow=10,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Proporciona una sesión de base de datos por petición.

    La sesión se crea al iniciar cada solicitud y se cierra automáticamente
    al finalizar, garantizando un uso limpio de los recursos.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
