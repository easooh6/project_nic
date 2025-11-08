from pydantic import BaseModel, ConfigDict
from datetime import time
from src.domain.enums.slot_status import TimeSlotStatus

class TimeSlot(BaseModel):

    id: int
    resource_id: int
    booking_id: int
    starts_at: time
    ends_at: time
    status: TimeSlotStatus

    model_config = ConfigDict(
        from_attributes=True
    )