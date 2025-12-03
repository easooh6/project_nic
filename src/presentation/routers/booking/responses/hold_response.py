from pydantic import BaseModel

class BookingHoldResponse(BaseModel):
    hold_id: str
    expires_at: int
