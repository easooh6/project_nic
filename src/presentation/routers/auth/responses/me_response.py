from pydantic import BaseModel, EmailStr
from src.domain.enums.role import RoleEnum

class MeResponse(BaseModel):

    email: EmailStr
    role: RoleEnum = RoleEnum.user