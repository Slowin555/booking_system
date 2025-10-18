import os
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, text


def main() -> None:
    database_url = os.getenv("DATABASE_URL", "postgresql://booking_user:booking_password@db:5432/booking_db")
    engine = create_engine(database_url)

    admin_id = str(uuid.uuid4())
    event_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    with engine.begin() as conn:
        # Ensure enums exist (safe if already created by migrations)
        # Insert admin user
        conn.execute(
            text(
                """
                INSERT INTO users (id, email, password_hash, role)
                VALUES (:id, :email, :password_hash, 'admin')
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {
                "id": admin_id,
                "email": "admin@example.com",
                "password_hash": "$2b$12$exampleexampleexampleexampleexampleexampleexampleexample",
            },
        )

        starts = datetime.now(timezone.utc) + timedelta(days=1)
        ends = starts + timedelta(hours=2)

        conn.execute(
            text(
                """
                INSERT INTO events (id, title, description, starts_at, ends_at, capacity, status, created_by)
                VALUES (:id, 'Sample Event', 'Seeded event', :starts, :ends, 10, 'published', :created_by)
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {"id": event_id, "starts": starts, "ends": ends, "created_by": admin_id},
        )

        # Insert a user and two bookings totaling <= capacity
        conn.execute(
            text(
                """
                INSERT INTO users (id, email, password_hash, role)
                VALUES (:id, 'user@example.com', :password_hash, 'user')
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {
                "id": user_id,
                "password_hash": "$2b$12$exampleexampleexampleexampleexampleexampleexampleexample",
            },
        )

        conn.execute(
            text(
                """
                INSERT INTO bookings (id, event_id, user_id, seats, status)
                VALUES (:id1, :event_id, :user_id, 2, 'active')
                """
            ),
            {"id1": str(uuid.uuid4()), "event_id": event_id, "user_id": user_id},
        )

        conn.execute(
            text(
                """
                INSERT INTO bookings (id, event_id, user_id, seats, status)
                VALUES (:id2, :event_id, :user_id, 3, 'active')
                """
            ),
            {"id2": str(uuid.uuid4()), "event_id": event_id, "user_id": user_id},
        )

    print("Seed completed.")


if __name__ == "__main__":
    main()


