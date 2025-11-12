from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=64)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True