from pydantic import BaseModel, EmailStr
from src.domain.enums.role import RoleEnum
from datetime import datetime

class UserRegisterResponse(BaseModel): # возвращаем данные пользователю
    id: int
    email: EmailStr
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True