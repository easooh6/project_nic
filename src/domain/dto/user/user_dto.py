from pydantic import BaseModel, EmailStr
from src.domain.enums.role import RoleEnum
from datetime import datetime

class UserDTO(BaseModel):
    
    id: int
    email: EmailStr
    is_active: bool = True
    role: RoleEnum = RoleEnum.user
    created_at: datetime

    model_config={
        "extra": "ignore"
    }