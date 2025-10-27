from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    location = Column(String(60), nullable=False)
    capacity = Column(Integer, nullable=False)
    file_path = Column(String(300))
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="resource")
    time_slots = relationship("TimeSlot", back_populates="resource")