from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, String, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class BookingStatusEnum(str):
    ACTIVE = "active"
    CANCELED = "canceled"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    status: Mapped[str] = mapped_column(Enum(BookingStatusEnum.ACTIVE, BookingStatusEnum.CANCELED, name="booking_status_enum"), nullable=False, default=BookingStatusEnum.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    event = relationship("Event", back_populates="bookings")
    user = relationship("User", back_populates="bookings")

    __table_args__ = (
        CheckConstraint("seats >= 1", name="bookings_seats_pos_chk"),
        Index("ix_bookings_event_status", "event_id", "status"),
        Index("ix_bookings_user_id", "user_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"Booking(id={self.id}, event_id={self.event_id}, user_id={self.user_id}, seats={self.seats}, status={self.status})"


