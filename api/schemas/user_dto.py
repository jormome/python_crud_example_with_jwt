"""Modelos de datos para la gestión de usuarios en la API."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Campos compartidos por los DTOs de entrada y salida de usuarios."""

    email: EmailStr = Field(...)
    is_active: bool = Field(default=True)


class UserCreateDto(UserBase):
    """DTO usado para crear un nuevo usuario desde una petición HTTP."""

    password: str = Field(..., min_length=5, max_length=100)


class UserResponseDto(UserBase):
    """DTO utilizado para devolver información pública del usuario."""

    id: int = Field(...)
    model_config = ConfigDict(from_attributes=True)
