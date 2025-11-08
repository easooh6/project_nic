from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.db.models.resource import Resource
from src.infrastructure.db.db import get_db_session

class ResourceRepository:
    def __init__(self):
        self.session_factory = get_db_session

    async def create(self,name: str, location: str, capacity: int, file_path: str | None = None) -> Resource:
        async with self.session_factory() as session:
            new_resource = Resource(
                name=name,
                location=location,
                capacity=capacity,
                file_path=file_path
                )
            session.add(new_resource)
            await session.flush()
            return new_resource

    async def get_by_id(self, resource_id: int) -> Resource | None:
        async with self.session_factory() as session:
            result = await session.execute(select(Resource).where(Resource.id == resource_id))
            return result.scalar_one_or_none()
        
    async def get_all(self) -> list[Resource]:
        async with self.session_factory() as session:
            result = await session.execute(select(Resource))
            return result.scalars().all()

    async def get_active(self) -> list[Resource]:
        async with self.session_factory() as session:
            result = await session.execute(select(Resource).where(Resource.is_active == True))
            return result.scalars().all()

    async def filter(self, capacity: int | None = None, location: str | None = None) -> list[Resource]:
        async with self.session_factory() as session:
            query = select(Resource).where(Resource.is_active == True)
            if capacity:
                query = query.where(Resource.capacity >= capacity)
            if location:
                query = query.where(Resource.location.ilike(f"%{location}%"))
            result = await session.execute(query)
            return result.scalars().all()

    async def update(self, resource_id: int, data: dict) -> Resource | None:
        async with self.session_factory() as session:
            result = await session.execute(select(Resource).where(Resource.id == resource_id))
            resource = result.scalar_one_or_none()
            if not resource:
                return None

            for key, value in data.items():
                if hasattr(resource, key):
                    setattr(resource, key, value)
            await session.flush()
            return resource

    async def delete(self, resource_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(Resource).where(Resource.id == resource_id))
            resource = result.scalar_one_or_none()
            if not resource:
                return False

            await session.delete(resource)
            await session.flush()
            return True
