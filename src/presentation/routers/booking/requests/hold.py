from pydantic import BaseModel
from datetime import datetime

class BookingHoldRequest(BaseModel):
    resource_id: int
    starts_at: datetime
    ends_at: datetime