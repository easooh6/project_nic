from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from src.domain.enums.role import RoleEnum

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: RoleEnum = RoleEnum.user

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True