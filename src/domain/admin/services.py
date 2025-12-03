from datetime import date
from typing import Iterable, Optional

from src.infrastructure.db.repositories.resource import ResourceRepository
from src.infrastructure.redis.repository import RedisRepository
from src.domain.admin.dto import (
    AdminResourceCreate,
    AdminResourceUpdate,
    AdminResourceRead,
)
from src.logger.logger import setup_logging

logger = setup_logging("app")


class AdminResourceService:
    def __init__(self) -> None:
        self.resource_repo = ResourceRepository()
        self.redis = RedisRepository()

    async def create_resource(self, data: AdminResourceCreate) -> AdminResourceRead:
        resource = await self.resource_repo.create(
            name=data.name,
            location=data.location,
            capacity=data.capacity,
            # file_path пока None – позже можно добавить загрузку файла
            file_path=None,
        )

        dto = AdminResourceRead.model_validate(resource)
        logger.debug("Admin created resource %s", str(dto.id))
        return dto

    async def update_resource(
        self,
        resource_id: int,
        data: AdminResourceUpdate,
        affected_dates: Optional[Iterable[date]] = None,
    ) -> Optional[AdminResourceRead]:
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        resource = await self.resource_repo.update(resource_id, update_data)
        if resource is None:
            logger.debug("Admin tried to update missing resource %s", str(resource_id))
            return None

        dto = AdminResourceRead.model_validate(resource)

        await self._invalidate_availability(resource_id, affected_dates)
        logger.debug("Admin updated resource %s", str(resource_id))
        return dto

    async def delete_resource(
        self,
        resource_id: int,
        affected_dates: Optional[Iterable[date]] = None,
    ) -> bool:
        deleted = await self.resource_repo.delete(resource_id)
        if not deleted:
            logger.debug("Admin tried to delete missing resource %s", str(resource_id))
            return False

        await self._invalidate_availability(resource_id, affected_dates)
        logger.debug("Admin deleted resource %s", str(resource_id))
        return True

    async def _invalidate_availability(
        self,
        resource_id: int,
        affected_dates: Optional[Iterable[date]] = None,
    ) -> None:
        if affected_dates is None:
            logger.debug(
                "",
            )
            return

        for d in affected_dates:
            key = f"avail:{resource_id}:{d.isoformat()}"
            await self.redis.delete(key)
            logger.debug(
                "Invalidate availability cache for %s at %s",
                str(resource_id),
                d.isoformat(),
            )
