class BaseBookingException(Exception):
    pass


class HoldAlreadyExistsException(BaseBookingException):
    def __init__(self):
        super().__init__("Hold already exists for this time range")


class TimeSlotUnavailableException(BaseBookingException):
    def __init__(self):
        super().__init__("One or more time slots are unavailable")

class HoldNotFoundException(BaseBookingException):
    def __init__(self):
        super().__init__("Hold not found or expired")


class SlotCollisionException(BaseBookingException):
    def __init__(self):
        super().__init__("Slot collision detected — booking cannot be confirmed")

class BookingNotFoundException(BaseBookingException):
    def __init__(self):
        super().__init__("Booking not found")

class BookingCancelForbiddenException(BaseBookingException):
    def __init__(self):
        super().__init__("You are not allowed to cancel this booking")
