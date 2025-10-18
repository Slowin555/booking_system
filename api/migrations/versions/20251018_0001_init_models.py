"""init models, enums, constraints, triggers

Revision ID: 20251018_0001
Revises: 
Create Date: 2025-10-18
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20251018_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enums
    role_enum = postgresql.ENUM("admin", "user", name="role_enum")
    role_enum.create(op.get_bind(), checkfirst=True)

    event_status_enum = postgresql.ENUM("draft", "published", "canceled", name="event_status_enum")
    event_status_enum.create(op.get_bind(), checkfirst=True)

    booking_status_enum = postgresql.ENUM("active", "canceled", name="booking_status_enum")
    booking_status_enum.create(op.get_bind(), checkfirst=True)

    # Tables
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", sa.Enum(name="role_enum"), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.execute("CREATE UNIQUE INDEX users_email_unique_ci ON users (lower(email));")

    op.create_table(
        "resources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("timezone", sa.String(), nullable=True),
    )
    op.create_index("ix_resources_name", "resources", ["name"], unique=True)

    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("status", sa.Enum(name="event_status_enum"), nullable=False, server_default="draft"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resources.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_events_starts_at", "events", ["starts_at"])
    op.create_index("ix_events_status", "events", ["status"])
    op.create_index("ix_events_created_by", "events", ["created_by"])
    op.create_check_constraint("events_time_order_chk", "events", "starts_at < ends_at")
    op.create_check_constraint("events_capacity_nonneg_chk", "events", "capacity >= 0")

    op.create_table(
        "bookings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("seats", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.Enum(name="booking_status_enum"), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_bookings_event_status", "bookings", ["event_id", "status"])
    op.create_index("ix_bookings_user_id", "bookings", ["user_id"])
    op.create_check_constraint("bookings_seats_pos_chk", "bookings", "seats >= 1")

    # Triggers
    op.execute(
        sa.text(
            """
            CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
            BEGIN
              NEW.updated_at := now();
              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER events_set_updated_at
            BEFORE UPDATE ON events
            FOR EACH ROW EXECUTE FUNCTION set_updated_at();
            """
        )
    )

    op.execute(
        sa.text(
            """
            CREATE OR REPLACE FUNCTION prevent_overbooking() RETURNS TRIGGER AS $$
            DECLARE
              current_capacity int;
              active_booked int;
            BEGIN
              PERFORM 1 FROM events WHERE id = NEW.event_id FOR UPDATE;

              SELECT capacity INTO current_capacity FROM events WHERE id = NEW.event_id;

              SELECT COALESCE(SUM(seats), 0) INTO active_booked
                FROM bookings
               WHERE event_id = NEW.event_id
                 AND status = 'active'
                 AND (TG_OP <> 'UPDATE' OR id <> NEW.id);

              IF (NEW.status = 'active') THEN
                IF (active_booked + NEW.seats) > current_capacity THEN
                  RAISE EXCEPTION 'Capacity exceeded for event %: %/% seats', NEW.event_id, active_booked + NEW.seats, current_capacity USING ERRCODE = '23514';
                END IF;
              END IF;

              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER bookings_prevent_overbooking_ins
            BEFORE INSERT ON bookings
            FOR EACH ROW EXECUTE FUNCTION prevent_overbooking();

            CREATE TRIGGER bookings_prevent_overbooking_upd
            BEFORE UPDATE ON bookings
            FOR EACH ROW EXECUTE FUNCTION prevent_overbooking();
            """
        )
    )


def downgrade() -> None:
    # Drop triggers and functions
    op.execute(sa.text("DROP TRIGGER IF EXISTS bookings_prevent_overbooking_upd ON bookings;"))
    op.execute(sa.text("DROP TRIGGER IF EXISTS bookings_prevent_overbooking_ins ON bookings;"))
    op.execute(sa.text("DROP FUNCTION IF EXISTS prevent_overbooking();"))
    op.execute(sa.text("DROP TRIGGER IF EXISTS events_set_updated_at ON events;"))
    op.execute(sa.text("DROP FUNCTION IF EXISTS set_updated_at();"))

    # Drop tables
    op.drop_index("ix_bookings_user_id", table_name="bookings")
    op.drop_index("ix_bookings_event_status", table_name="bookings")
    op.drop_table("bookings")

    op.drop_constraint("events_capacity_nonneg_chk", "events", type_="check")
    op.drop_constraint("events_time_order_chk", "events", type_="check")
    op.drop_index("ix_events_created_by", table_name="events")
    op.drop_index("ix_events_status", table_name="events")
    op.drop_index("ix_events_starts_at", table_name="events")
    op.drop_table("events")

    op.drop_index("ix_resources_name", table_name="resources")
    op.drop_table("resources")

    op.execute("DROP INDEX IF EXISTS users_email_unique_ci;")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS booking_status_enum;")
    op.execute("DROP TYPE IF EXISTS event_status_enum;")
    op.execute("DROP TYPE IF EXISTS role_enum;")


