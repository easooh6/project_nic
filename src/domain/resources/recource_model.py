from sqlalchemy import Column, Integer, String, Boolean
from domain.resources.settings import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    file_path = Column(String(255))
    is_active = Column(Boolean, default=True)
