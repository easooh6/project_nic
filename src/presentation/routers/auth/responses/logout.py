from pydantic import BaseModel

class LogoutResponse(BaseModel):
    status: bool = True
    message: str = "Logout successful"

    class Config:
        from_attributes = True    