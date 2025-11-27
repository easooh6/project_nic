from pydantic import BaseModel, EmailStr, Field
from src.domain.enums.role import RoleEnum


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: RoleEnum = RoleEnum.user

    class Config:
        from_attributes = True
