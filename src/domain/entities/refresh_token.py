from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RefreshToken(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    expires_at: datetime
    revoked: bool

    model_config = ConfigDict(
        from_attributes=True
    )
