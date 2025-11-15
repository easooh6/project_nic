from pydantic import BaseModel, EmailStr, Field, ConfigDict
from src.domain.enums.role import RoleEnum
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: RoleEnum = RoleEnum.user


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: RoleEnum
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserResponse


class LoginResponse(BaseModel):
    access: str  # Пока фейковый токен "todo"
    user: UserResponse