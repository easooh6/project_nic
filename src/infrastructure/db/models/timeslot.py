from src.infrastructure.db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Time, Enum as SqlEnum
from datetime import time
from src.domain.enums.slot_status import TimeSlotStatus

class TimeSlot(Base):

    __tablename__ = "time_slot"

    id: Mapped[int] = mapped_column(primary_key=True)
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey('resource.id'))
    booking_id: Mapped[int] = mapped_column(ForeignKey('booking.id', ondelete="SET NULL"), nullable=True)
    starts_at: Mapped[time] = mapped_column(Time, nullable=False)
    ends_at: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[TimeSlotStatus] = mapped_column(
                                        SqlEnum(TimeSlotStatus,
                                        name='timeslotstatus'),
                                        default=TimeSlotStatus.AVAILABLE
                                        )
    
    booking: Mapped['Booking'] = relationship('Booking', back_populates='time_slots')
    resource: Mapped['Resource'] = relationship('Resource', back_populates='time_slots')