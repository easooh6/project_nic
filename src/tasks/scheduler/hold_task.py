from src.tasks.broker import broker
from taskiq import TaskiqDepends
from src.domain.booking.booking_service import BookingService
from src.logger.logger import setup_logging
from src.presentation.di.service.scheduler.booking import get_booking_service

logger = setup_logging("app")

@broker.task(schedule=[
    {"cron": "*/5 * * * *"}
            ])
async def release_holds(service: BookingService = TaskiqDepends(get_booking_service)):
    try:
        logger.info("Release-holds was started(cron task)")
        updated_slots = await service.update_overdue_ids()

        logger.info("%d slots were updated to available(cron task)", updated_slots)

        return updated_slots
    except Exception as e:
        logger.error("Error during release_holds: %s", e)
        return 0
