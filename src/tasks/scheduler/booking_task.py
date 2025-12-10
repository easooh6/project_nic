from src.tasks.broker import broker
from src.domain.booking.booking_service import BookingService
from taskiq import TaskiqDepends
from src.presentation.di.service.scheduler.booking import get_booking_service
from src.logger.logger import setup_logging

logger = setup_logging("app")

@broker.task(schedule=[
    {"cron": "0 0 0 * *"}
            ])
async def archive_bookings_task(service: BookingService = TaskiqDepends(get_booking_service)):
    
    try:
        logger.info("Booking(booking cron task)")

        updated_rows = await service.update_available_bookings_to_archived()

        logger.info("%d rows are updated(booking cron task)", updated_rows)

        return updated_rows
    
    except Exception as e:
        logger.error("Error during archive_bookings: %s", e)
        return
