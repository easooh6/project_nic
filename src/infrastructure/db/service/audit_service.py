from typing import Any

from sqlalchemy.orm import Session

from models.audit_log import AuditLog


def log_action(
    db: Session,
    *,
    actor_user_id: int | None,
    action: str,
    entity: str,
    entity_id: int | None,
    meta: dict[str, Any] | None = None,
) -> AuditLog:
    
    record = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        meta=meta or {},
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
