from pydantic import BaseModel

class RefreshResponse(BaseModel):
    access: str

    model_config = {
        "from_attributes": True
    }