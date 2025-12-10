from src.infrastructure.db.db import get_db_session
from typing import Callable, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from src.domain.entities.timeslot import TimeSlot
from src.infrastructure.db.models.timeslot import TimeSlot as TimeSlotModel
from datetime import time
from src.domain.enums.slot_status import TimeSlotStatus

class TimeSlotRepository:

    def __init__(self):
        self.session_factory: Callable[[], AsyncContextManager[AsyncSession]] = get_db_session

    async def create_time_slot(self, entity: TimeSlot) -> TimeSlotModel | None:

        async with self.session_factory() as session:
            
            query_check = select(TimeSlotModel).where(
                TimeSlotModel.resource_id==entity.resource_id,
                TimeSlotModel.starts_at==entity.starts_at,
                TimeSlotModel.ends_at==entity.ends_at)
            
            check_result = (await session.execute(query_check)).scalar_one_or_none()

            if check_result:
                return None
            
            model = TimeSlotModel(**entity.model_dump())
            session.add(model)

            await session.flush()
            await session.refresh(model)

            entity = TimeSlot.model_validate(model)

            return entity

    async def get_time_slots_by_resource_id(self, resource_id: int) -> list[TimeSlot]:

        async with self.session_factory() as session:

            query = select(TimeSlotModel).where(TimeSlotModel.resource_id==resource_id)

            models = (await session.execute(query)).scalars().all()
            entities = [TimeSlot.model_validate(model) for model in models]

            return entities
    
    async def get_overdue_slots(self, ttl: int) -> list[int]:
        
        async with self.session_factory() as session:

            query = select(TimeSlotModel.id).where(TimeSlotModel.status == TimeSlotStatus.HELD,
                                           func.extract('epoch', func.now() - TimeSlotModel.starts_at) > ttl)

            ids = (await session.execute(query)).scalars().all()

            return ids


    async def update_held_slots(self, ids: list[int]) -> int:
        
        async with self.session_factory() as session:

            query = update(TimeSlotModel).where(
                TimeSlotModel.id.in_(ids)).values(
                    status=TimeSlotStatus.AVAILABLE
                    )

            result = await session.execute(query)

            return result.rowcount

    async def get_time_slot_by_time(self, resource_id: int | None,
                                     starts_at: time, ends_at: time) -> list[TimeSlot]:
        
        async with self.session_factory() as session:

            if resource_id is not None:
                query = select(TimeSlotModel).where(
                    TimeSlotModel.resource_id==resource_id,
                    TimeSlotModel.starts_at==starts_at,
                    TimeSlotModel.ends_at==ends_at
                )
            
            else:
                query = select(TimeSlotModel).where(
                    TimeSlotModel.starts_at==starts_at,
                    TimeSlotModel.ends_at==ends_at
                )
            
            models = (await session.execute(query)).scalars().all()
            entities = [TimeSlot.model_validate(model) for model in models]

            return entities
        
    async def update_time_slot_status(self, entity: TimeSlot, booking_id: int = None) -> int:

        async with self.session_factory() as session:
            
            if booking_id is None:
                query = update(TimeSlotModel).where(TimeSlotModel.id == entity.id).values(
                        status=entity.status
                    )
            else:
                query = update(TimeSlotModel).where(TimeSlotModel.id == entity.id).values(
                    status=entity.status,
                    booking_id=booking_id
                )

            result = await session.execute(query)
 
            return result.rowcount

    async def delete_time_slot_by_id(self, id: int) -> int:

        async with self.session_factory() as session:

            query = delete(TimeSlotModel).where(TimeSlotModel.id==id)
            result = await session.execute(query)
            
            return result.rowcount

