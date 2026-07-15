"""Database configuration"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session

from ..exceptions.exceptions import ConnectionException
from .settings import settings

if not settings.DATABASE_URI:
    raise ConnectionException("DATABASE_URI no está configurada")

engine: Engine = create_engine(
    settings.DATABASE_URI,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
