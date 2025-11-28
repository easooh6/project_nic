from pydantic import BaseModel
from datetime import time
from src.domain.enums.slot_status import TimeSlotStatus

class AvailabilitySlot(BaseModel):
    id: int
    starts_at: time
    ends_at: time
    status: TimeSlotStatus

class AvailabilityResponse(BaseModel):
    slots: list[AvailabilitySlot]
