from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modules.users.models import UserRole


class UserRegistration(BaseModel):
    """
    Request body for user registration.
    """

    full_name: str = Field(
        min_length=2,
        max_length=255,
        examples=["Ram Gupta"],
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["StrongPassword123!"],
    )


class UserLogin(BaseModel):
    """
    Request body for user login.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Authentication token response.
    """

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """
    Public user response.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool