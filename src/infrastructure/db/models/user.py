from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.db.models.base import Base
from src.domain.enums.role import RoleEnum


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum, name="userrole"), default=RoleEnum.user, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")
    file_uploads: Mapped[list["FileUpload"]] = relationship("FileUpload", back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user")
    
    __table_args__ = (
        Index("ix_user_created_at", "created_at"),
    )