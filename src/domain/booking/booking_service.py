import uuid
from datetime import datetime, timedelta, date
from src.infrastructure.redis.repository import RedisRepository
from src.infrastructure.db.repositories.timeslot import TimeSlotRepository
from src.infrastructure.db.repositories.booking import BookingRepository

from src.domain.entities.booking import Booking
from src.domain.enums.booking_status import BookingStatus
from src.domain.enums.slot_status import TimeSlotStatus
from src.domain.exceptions.booking.booking import (
    TimeSlotUnavailableException, 
    HoldAlreadyExistsException, 
    BookingNotFoundException,
    SlotCollisionException,
    HoldNotFoundException,
    BookingCancelForbiddenException
)
from src.logger.logger import setup_logging

logger = setup_logging("app")

class BookingService:
    HOLD_TTL_SECONDS = 120  
    HOLD_REDIS_PREFIX = "hold:"

    def __init__(self):
        self.redis = RedisRepository()
        self.timeslot_repo = TimeSlotRepository()
        self.booking_repo = BookingRepository()
        


    async def hold(self, resource_id: int, starts_at, ends_at, user_id: int):
        lock_key = f"hold:{resource_id}:{starts_at}-{ends_at}"

        if await self.redis.exists(lock_key):
            raise HoldAlreadyExistsException()

        # get slots
        slots = await self.timeslot_repo.get_time_slot_by_time(
            resource_id=resource_id,
            starts_at=starts_at,
            ends_at=ends_at
        )

        # availability check
        for slot in slots:
            if slot.status != TimeSlotStatus.AVAILABLE:
                raise TimeSlotUnavailableException()

        await self.redis.set(lock_key, "1", ttl=self.HOLD_TTL_SECONDS)

        # update status
        for slot in slots:
            slot.status = TimeSlotStatus.HELD
            await self.timeslot_repo.update_time_slot_status(slot)

        hold_id = str(uuid.uuid4())

        expires_at = datetime.utcnow() + timedelta(seconds=self.HOLD_TTL_SECONDS)

        return {"hold_id": hold_id, "expires_at": expires_at}


    async def confirm(self, user_id: int, hold_id: str):
        redis_key = f"{self.HOLD_REDIS_PREFIX}{hold_id}"
        hold_data = await self.redis.get(redis_key)

        if hold_data is None:
            raise HoldNotFoundException()

        import json
        hold_data = json.loads(hold_data)

        resource_id = hold_data["resource_id"]
        starts_at = datetime.fromisoformat(hold_data["starts_at"])
        ends_at = datetime.fromisoformat(hold_data["ends_at"])

        slots = await self.timeslot_repo.get_time_slot_by_time(
            resource_id=resource_id,
            starts_at=starts_at.time(),
            ends_at=ends_at.time()
        )

        if not slots or any(s.status != TimeSlotStatus.HELD for s in slots):
            raise TimeSlotUnavailableException()

        booked_slots = await self.timeslot_repo.get_time_slot_by_time(
            resource_id=resource_id,
            starts_at=starts_at.time(),
            ends_at=ends_at.time()
        )

        if any(s.status == TimeSlotStatus.BOOKED for s in booked_slots):
            raise SlotCollisionException()

        booking_entity = Booking(
            user_id=user_id,
            resource_id=resource_id,
            starts_at=starts_at,
            ends_at=ends_at,
            status=BookingStatus.CONFIRMED,
            created_at=datetime.utcnow()
        )

        booking = await self.booking_repo.create_booking(booking_entity)

        for slot in slots:
            slot.status = TimeSlotStatus.BOOKED
            await self.timeslot_repo.update_time_slot_status(slot, booking.id)

        await self.redis.delete(redis_key)

        return booking


    async def cancel(self, user_id: int, booking_id: int) -> None:
        booking = await self.booking_repo.get_booking_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundException()

        if booking.user_id != user_id:
            raise BookingCancelForbiddenException()

        slots = await self.timeslot_repo.get_time_slot_by_time(
            resource_id=booking.resource_id,
            starts_at=booking.starts_at,
            ends_at=booking.ends_at
        )

        for slot in slots:
            slot.status = TimeSlotStatus.AVAILABLE
            await self.timeslot_repo.update_time_slot_status(slot)

        booking.status = BookingStatus.CANCELLED
        await self.booking_repo.update_booking_status(booking)

        return None


    async def get_my_bookings(self, user_id: int):
        bookings = await self.booking_repo.get_booking_by_user_id(user_id)
        if bookings is None:
            return []
        return bookings
    

    async def get_availability(self, resource_id: int, requested_date: date):
        key = f"avail:{resource_id}:{requested_date}"

        cached = await self.redis.get(key)
        if cached:
            return cached

        slots = await self.timeslot_repo.get_time_slots_by_resource_id(resource_id)

        filtered = [
            s for s in slots
            if s.starts_at.date() == requested_date
            and s.status == TimeSlotStatus.available
        ]

        response = [
            {
                "id": s.id,
                "starts_at": s.starts_at,
                "ends_at": s.ends_at,
                "status": s.status,
            }
            for s in filtered
        ]

        await self.redis.set(key, response, ttl=60)

        return response
    
    async def update_available_bookings_to_archived(self) -> int:
        
        ids = await self.booking_repo.get_available_bookings()

        if not ids:
            logger.debug("No available bookings found")
            return 0
        
        updated_rows = await self.booking_repo.update_booking_status_to_archived(ids)

        return updated_rows

    async def update_overdue_ids(self) -> int:

        ids = await self.timeslot_repo.get_overdue_slots(self.HOLD_TTL_SECONDS)

        if not ids:
            logger.debug("No overdue slots to release")
            return 0
        
        updated_rows = await self.timeslot_repo.update_held_slots(ids)
        
        return updated_rows

# obj = BookingService()
# import asyncio
# asyncio.run(obj.update_available_bookings_to_archived())