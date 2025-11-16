from pydantic import BaseModel, EmailStr, Field
from src.domain.enums.role import RoleEnum
from datetime import datetime

class UserDTO(BaseModel):
    
    id: int
    email: EmailStr
    is_active: bool = True
    role: RoleEnum = RoleEnum.user
    created_at: datetime

    model_config={
        "extra": "ignore",
        "from_attributes": True
    }

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