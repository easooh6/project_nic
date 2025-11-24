from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from src.domain.enums.role import RoleEnum


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    access_token: str
    # refresh_token: str  # TODO
    token_type: str = "Bearer"
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)


class RegisterResponse(BaseModel):
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)
