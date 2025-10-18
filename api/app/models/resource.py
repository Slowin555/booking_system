from __future__ import annotations

from typing import List, Optional
from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    timezone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    events: Mapped[List["Event"]] = relationship(back_populates="resource")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Resource(id={self.id}, name={self.name})"


