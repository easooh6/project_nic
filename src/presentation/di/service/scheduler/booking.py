from src.domain.booking.booking_service import BookingService

async def get_booking_service() -> BookingService:
    return BookingService()