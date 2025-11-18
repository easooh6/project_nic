from pydantic import BaseModel, EmailStr
from src.domain.enums.role import RoleEnum
from datetime import datetime

class User(BaseModel):

    id: int
    email: EmailStr
    password_hash: int
    is_active: bool
    role: RoleEnum
    created_at: datetime
    updated_at: datetime
    
    model_config= {
        "from_attributes": True
    }