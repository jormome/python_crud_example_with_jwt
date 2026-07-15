"""
DTOs for user operations.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """
    Base schema for user operations.
    """

    email: EmailStr = Field(..., description="User email")
    is_active: bool = Field(default=True, description="is an active user")


class UserCreateDto(UserBase):
    """
    Create schema for new user.
    """

    password: str = Field(..., description="User password")


class UserUpdateDto(BaseModel):
    """
    Update schema for user - all fields optional for partial updates.
    """

    email: EmailStr | None = Field(None, description="User email")
    password: str | None = Field(None, description="User password")
    is_active: bool | None = Field(None, description="is an active user")


class UserResponseDto(UserBase):
    """
    Response schema for user.
    """

    id: int = Field(..., description="User ID")
    model_config = ConfigDict(from_attributes=True)
