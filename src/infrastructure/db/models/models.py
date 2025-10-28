from ..database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class FileUpload(Base):
    __tablename__ = "file_uploads"
    id = Column(Integer, primary_key=True, index=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"))
    path = Column(String)
    size_bytes = Column(Integer)
    mime = Column(String)
    created_at = Column(DateTime, default=func.now())


