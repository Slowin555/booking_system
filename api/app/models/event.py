from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, String, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class EventStatusEnum(str):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELED = "canceled"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(Enum(EventStatusEnum.DRAFT, EventStatusEnum.PUBLISHED, EventStatusEnum.CANCELED, name="event_status_enum"), nullable=False, default=EventStatusEnum.DRAFT)
    created_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    resource_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    created_by_user = relationship("User", back_populates="events_created")
    resource = relationship("Resource", back_populates="events")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="event", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("starts_at < ends_at", name="events_time_order_chk"),
        CheckConstraint("capacity >= 0", name="events_capacity_nonneg_chk"),
        Index("ix_events_starts_at", "starts_at"),
        Index("ix_events_status", "status"),
        Index("ix_events_created_by", "created_by"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"Event(id={self.id}, title={self.title}, status={self.status})"


