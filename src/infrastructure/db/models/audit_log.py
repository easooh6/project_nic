from sqlalchemy import ForeignKey, JSON, DateTime, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.db.models import Base 


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100))
    entity: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[int] = mapped_column(Integer)
    meta: Mapped[dict] = mapped_column(JSON)
    ts: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    actor_user = relationship("User", back_populates="audit_logs")
