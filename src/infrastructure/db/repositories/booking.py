from src.infrastructure.db.db import get_db_session
from src.domain.entities.booking import Booking
from src.infrastructure.db.models.booking import Booking as BookingModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Callable, AsyncContextManager
from datetime import datetime, timedelta
from src.domain.enums.booking_status import BookingStatus

class BookingRepository:

    def __init__(self):
        self.session_factory: Callable[[], AsyncContextManager[AsyncSession]] = get_db_session
    
    async def create_booking(self, entity: Booking) -> Booking:
        
        async with self.session_factory() as session:

            booking_model = BookingModel(**entity.model_dump())
            session.add(booking_model)

            await session.flush()
            await session.refresh(booking_model)

            entity = Booking.model_validate(booking_model)

            return entity
    
    async def get_booking_by_id(self, id: int) -> Booking | None:

        async with self.session_factory() as session:

            query = select(BookingModel).where(BookingModel.id==id)
            model = (await session.execute(query)).scalar_one_or_none()
            if not model:
                return None
            
            return Booking.model_validate(model)
        
    async def get_bookings_by_date(self, user_id: int, start_date: datetime,
                                     end_date: datetime | None = None) -> list[Booking] | None:
        
        async with self.session_factory() as session:

            if end_date is None:

                query = select(BookingModel).where(
                    BookingModel.user_id == user_id,
                    BookingModel.created_at >= start_date,
                    BookingModel.created_at < start_date + timedelta(days=1)
                )
            else:

                query = select(BookingModel).where(
                    BookingModel.user_id == user_id,
                    BookingModel.created_at >= start_date,
                    BookingModel.created_at <= end_date
                )

            models_raw = (await session.execute(query)).scalars().all()
            if not models_raw:
                return None

            models = [Booking.model_validate(model) for model in models_raw]

            return models
    
    async def get_booking_by_status(self, user_id: int, status: BookingStatus) -> list[Booking] | None:

        async with self.session_factory() as session:

            query = select(BookingModel).where(
                BookingModel.user_id==user_id,
                BookingModel.status==status
                )
            
            models_raw = (await session.execute(query)).scalars().all()

            if not models_raw:
                return None
            
            models = [Booking.model_validate(model) for model in models_raw]

            return models
        
    async def get_booking_by_user_id(self, user_id: int) -> list[Booking] | None:

        async with self.session_factory() as session:

            query = select(BookingModel).where(BookingModel.user_id==user_id)
            models_raw = (await session.execute(query)).scalars().all()

            models = [Booking.model_validate(model) for model in models_raw]

            if not models:
                return None

            return models   
        
    async def update_booking_status(self, entity: Booking) -> int:

        async with self.session_factory() as session:

            query = update(BookingModel).where(BookingModel.id == entity.id).values(
                    status=entity.status
                )
            result = await session.execute(query)
 
            return result.rowcount

    async def delete_booking_by_id(self, id: int) -> int:

        async with self.session_factory() as session:

            query = delete(BookingModel).where(BookingModel.id==id)
            result = await session.execute(query)
            
            return result.rowcount
            

    async def delete_booking_by_user_id(self, user_id: int):

        async with self.session_factory() as session:

            query = delete(BookingModel).where(BookingModel.user_id==user_id)
            result = await session.execute(query)

            return result.rowcount