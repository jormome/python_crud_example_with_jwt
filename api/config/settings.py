"""Global configuration management"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carga y valida la configuracion desde las variables de entorno

    Args:
        BaseSettings (_type_): _description_
    """

    DATABASE_URI: str = Field(default="")
    SECRET_KEY: str = Field(default="")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    BCRYPT_ROUNDS: int = Field(default=12)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
