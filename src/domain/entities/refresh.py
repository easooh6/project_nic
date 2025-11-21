from pydantic import BaseModel
from datetime import datetime

class RefreshEntity(BaseModel):

    id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime
    revoked: bool = False

    model_config= {
        "from_attributes": True
    }