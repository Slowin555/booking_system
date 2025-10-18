from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Re-export models for convenience
from .user import User, RoleEnum  # noqa: E402,F401
from .resource import Resource  # noqa: E402,F401
from .event import Event, EventStatusEnum  # noqa: E402,F401
from .booking import Booking, BookingStatusEnum  # noqa: E402,F401


