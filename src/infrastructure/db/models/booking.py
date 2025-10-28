from src.infrastructure.db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Enum as SqlEnum
from datetime import datetime
from src.domain.enums.booking_status import BookingStatus
from typing import List

class Booking(Base):

    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id"))
    timeslot_id: Mapped[int] = mapped_column(ForeignKey("time_slot.id"))
    status: Mapped[BookingStatus] = mapped_column(
                                        SqlEnum(BookingStatus, 
                                        name="bookingstatus"),
                                        default=BookingStatus.CONFIRMED
                                        )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    time_slots: Mapped[List['TimeSlot']] = relationship('TimeSlot', back_populates='booking')
    resource: Mapped['Resource'] = relationship('Resource', back_populates='booking')
    user: Mapped['User'] = relationship('User', back_populates='booking')