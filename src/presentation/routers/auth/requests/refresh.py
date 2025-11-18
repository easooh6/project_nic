from pydantic import BaseModel

class RefreshRequest(BaseModel):
    refresh: str

    model_config = {
        "from_attributes": True
    }