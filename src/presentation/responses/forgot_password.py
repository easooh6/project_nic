from pydantic import BaseModel

class ForgotPasswordResponse(BaseModel):
    message: str
    email: str

    class Config:
        from_attributes = True
