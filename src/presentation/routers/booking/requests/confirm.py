from pydantic import BaseModel

class BookingConfirmRequest(BaseModel):
    hold_id: str
