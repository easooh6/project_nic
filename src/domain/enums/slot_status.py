from enum import Enum

class TimeSlotStatus(Enum):
    
    AVAILABLE = "available"
    HELD = "held"
    BOOKED = "booked"