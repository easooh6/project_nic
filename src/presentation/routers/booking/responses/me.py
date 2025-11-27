from pydantic import BaseModel
from datetime import datetime
from src.domain.enums.booking_status import BookingStatus

class BookingMeItem(BaseModel):
    id: int
    resource_id: int
    starts_at: datetime
    ends_at: datetime
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True


class BookingMeResponse(BaseModel):
    bookings: list[BookingMeItem]
