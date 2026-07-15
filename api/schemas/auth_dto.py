"""
DTOs for auth operations.
"""

from pydantic import BaseModel, EmailStr


class LoginRequestDto(BaseModel):
    """
    Request schema for login. Contains email and password from the user.
    """

    email: EmailStr
    password: str


class LoginResponseDto(BaseModel):
    """
    Response schema for login. Returns the token and its type after authentication.
    """

    access_token: str
    token_type: str = "bearer"
