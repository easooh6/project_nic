from pydantic import BaseModel

class ResetPasswordResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True
