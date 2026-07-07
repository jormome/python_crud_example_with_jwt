"""Modelos de datos para el flujo de autenticación con JWT."""

from pydantic import BaseModel, EmailStr


class LoginRequestDto(BaseModel):
    """DTO con las credenciales enviadas para iniciar sesión."""

    email: EmailStr
    password: str


class LoginResponseDto(BaseModel):
    """DTO que devuelve el token de acceso después de autenticar."""

    access_token: str
    token_type: str = "bearer"
