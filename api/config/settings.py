"""Gestión de configuraciones globales de la aplicación."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Carga y valida la configuración desde variables de entorno."""

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_MINUTES: int = 60
    DATABASE_URI: str = "sqlite:///./db.sqlite"
    BCRYPT_ROUNDS: int = 12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
