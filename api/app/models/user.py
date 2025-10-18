from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class RoleEnum(str):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(Enum(RoleEnum.ADMIN, RoleEnum.USER, name="role_enum"), nullable=False, default=RoleEnum.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    events_created: Mapped[List["Event"]] = relationship(back_populates="created_by_user")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("email <> ''", name="users_email_not_empty_chk"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"User(id={self.id}, email={self.email}, role={self.role})"


