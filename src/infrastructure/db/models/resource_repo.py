from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.db.models.resource import Resource
import logging
logger = logging.getLogger(__name__)

class ResourceRepository:
    async def create(self, session: AsyncSession, name: str, location: str, capacity: int, file_path: str | None = None) -> Resource:
        new_resource = Resource(
            name=name,
            location=location,
            capacity=capacity,
            file_path=file_path
            )
        session.add(new_resource)
        await session.flush()
        return new_resource

    async def get_by_id(self, session: AsyncSession, resource_id: int) -> Resource | None:
        result = await session.execute(select(Resource).where(Resource.id == resource_id))
        return result.scalar_one_or_none()
    async def get_all(self, session: AsyncSession) -> list[Resource]:
        result = await session.execute(select(Resource))
        return result.scalars().all()

    async def get_active(self, session: AsyncSession) -> list[Resource]:
        result = await session.execute(select(Resource).where(Resource.is_active == True))
        return result.scalars().all()

    async def filter(self, session: AsyncSession, capacity: int | None = None, location: str | None = None) -> list[Resource]:
        query = select(Resource).where(Resource.is_active == True)
        if capacity:
            query = query.where(Resource.capacity >= capacity)
        if location:
            query = query.where(Resource.location.ilike(f"%{location}%"))
        result = await session.execute(query)
        return result.scalars().all()

    async def update(self, session: AsyncSession, resource_id: int, data: dict) -> Resource | None:
        result = await session.execute(select(Resource).where(Resource.id == resource_id))
        resource = result.scalar_one_or_none()
        if not resource:
            return None

        for key, value in data.items():
            if hasattr(resource, key):
                setattr(resource, key, value)

        logger.info(f"Cache invalidated for resource id={resource_id}")
        await session.flush()
        return resource

    async def delete(self, session: AsyncSession, resource_id: int) -> bool:
        result = await session.execute(select(Resource).where(Resource.id == resource_id))
        resource = result.scalar_one_or_none()
        if not resource:
            return False

        await session.delete(resource)
        await session.flush()
        return True
