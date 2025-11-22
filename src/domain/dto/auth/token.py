from pydantic import BaseModel
from datetime import datetime
from src.domain.enums.role import RoleEnum

class TokenDTO(BaseModel):

<<<<<<< HEAD
    sub: str
=======
    sub: int
>>>>>>> 8e88b8e6dba6e6c36e2d9bca05367e3ccf7dfe7c
    role: RoleEnum
    type: str = "access"
    exp: datetime

