from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base import Base 


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    actor_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String, nullable=False, index=True)
    entity = Column(String, nullable=False, index=True)
    entity_id = Column(BigInteger, nullable=True, index=True)
    meta = Column(JSON, nullable=True)
    ts = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    actor_user = relationship(
        "User",
        back_populates="audit_logs",
    )

    __table_args__ = (
        Index("ix_auditlog_entity_lookup", "entity", "entity_id"),
        Index("ix_auditlog_actor_time", "actor_user_id", "ts"),
    )
