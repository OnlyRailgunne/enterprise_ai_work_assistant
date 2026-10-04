import uuid
from datetime import datetime

from app.db import get_connection


def create_event(
    title,
    start_time,
    end_time,
    description=None,
    location=None,
    organizer_id=None,
):
    event_id = uuid.uuid4()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO events (
                    id,
                    title,
                    description,
                    start_time,
                    end_time,
                    location,
                    organizer_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    title,
                    description,
                    start_time,
                    end_time,
                    location,
                    organizer_id,
                    created_at,
                    updated_at
                """,
                (
                    event_id,
                    title,
                    description,
                    start_time,
                    end_time,
                    location,
                    organizer_id,
                ),
            )

            row = cursor.fetchone()

    return _event_from_row(row)


def get_event(event_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    start_time,
                    end_time,
                    location,
                    organizer_id,
                    created_at,
                    updated_at
                FROM events
                WHERE id = %s
                """,
                (event_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return _event_from_row(row)


def list_events(
    organizer_id=None,
):
    query = """
        SELECT
            id,
            title,
            description,
            start_time,
            end_time,
            location,
            organizer_id,
            created_at,
            updated_at
        FROM events
    """

    values = []

    if organizer_id is not None:
        query += " WHERE organizer_id = %s"
        values.append(organizer_id)

    query += " ORDER BY start_time ASC"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            rows = cursor.fetchall()

    return [_event_from_row(row) for row in rows]


def cancel_event(event_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM events
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    start_time,
                    end_time,
                    location,
                    organizer_id,
                    created_at,
                    updated_at
                """,
                (event_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return _event_from_row(row)


def _event_from_row(row):
    return {
        "id": str(row[0]),
        "title": row[1],
        "description": row[2],
        "start_time": (
            row[3].isoformat()
            if isinstance(row[3], datetime)
            else row[3]
        ),
        "end_time": (
            row[4].isoformat()
            if isinstance(row[4], datetime)
            else row[4]
        ),
        "location": row[5],
        "organizer_id": row[6],
        "created_at": (
            row[7].isoformat()
            if row[7]
            else None
        ),
        "updated_at": (
            row[8].isoformat()
            if row[8]
            else None
        ),
    }