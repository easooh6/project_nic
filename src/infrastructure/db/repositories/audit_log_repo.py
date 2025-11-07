from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_log(
        self,
        *,
        actor_user_id: int,
        action: str,
        entity: str,
        entity_id: int,
        changes: Optional[dict] = None,
    ) -> AuditLog:
        log = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            entity=entity,
            entity_id=entity_id,
            changes=changes,
        )
        self.session.add(log)
        await self.session.commit()
        # чтобы получить id и прочие значения из БД
        await self.session.refresh(log)
        return log

    async def get_logs(
        self,
        *,
        actor_user_id: Optional[int] = None,
        entity: Optional[str] = None,
        entity_id: Optional[int] = None,
        action: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLog)

        if actor_user_id is not None:
            stmt = stmt.where(AuditLog.actor_user_id == actor_user_id)
        if entity is not None:
            stmt = stmt.where(AuditLog.entity == entity)
        if entity_id is not None:
            stmt = stmt.where(AuditLog.entity_id == entity_id)
        if action is not None:
            stmt = stmt.where(AuditLog.action == action)

        stmt = stmt.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all()
