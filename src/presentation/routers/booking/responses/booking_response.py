from pydantic import BaseModel
from datetime import datetime
from src.domain.enums.booking_status import BookingStatus

class BookingResponse(BaseModel):
    id: int
    resource_id: int
    starts_at: datetime
    ends_at: datetime
    status: BookingStatus
    created_at: datetime
