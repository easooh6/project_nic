from ..database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

class RoleEnum(str, PyEnum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)

    __table_args__ = (
        Index("ix_user_created_at", "created_at"),
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    user = relationship("User", back_populates="refresh_tokens")
    revoked = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        Index("ix_token_user_expires", "user_id", "expires_at"),
    )