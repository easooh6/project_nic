from pydantic import BaseModel, ConfigDict
from src.domain.enums.booking_status import BookingStatus
from datetime import datetime

class Booking(BaseModel):
    
    id: int
    user_id: int
    resource_id: int
    status: BookingStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
