from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    location = Column(String(60), nullable=False)
    capacity = Column(Integer, nullable=False)
    file_path = Column(String(300))
    is_active = Column(Boolean, default=True)
