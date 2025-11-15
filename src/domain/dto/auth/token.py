from pydantic import BaseModel
from datetime import datetime
from src.domain.enums.role import RoleEnum

class TokenDTO(BaseModel):

    sub: str
    role: RoleEnum
    type: str = "access"
    exp: datetime

