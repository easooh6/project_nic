from pydantic import BaseModel, Field

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6, max_length=128)

    class Config:
        from_attributes = True
