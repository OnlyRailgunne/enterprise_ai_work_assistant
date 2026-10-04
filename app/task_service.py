import uuid
from datetime import date

from app.db import get_connection


def create_task(
    title,
    description=None,
    status="pending",
    priority="medium",
    assignee_id=None,
    due_date=None,
):
    task_id = uuid.uuid4()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (
                    id,
                    title,
                    description,
                    status,
                    priority,
                    assignee_id,
                    due_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    title,
                    description,
                    status,
                    priority,
                    assignee_id,
                    due_date,
                    created_at,
                    updated_at
                """,
                (
                    task_id,
                    title,
                    description,
                    status,
                    priority,
                    assignee_id,
                    due_date,
                ),
            )

            row = cursor.fetchone()

    return _task_from_row(row)


def get_task(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    status,
                    priority,
                    assignee_id,
                    due_date,
                    created_at,
                    updated_at
                FROM tasks
                WHERE id = %s
                """,
                (task_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return _task_from_row(row)


def list_tasks(
    assignee_id=None,
    status=None,
):
    conditions = []
    values = []

    if assignee_id is not None:
        conditions.append("assignee_id = %s")
        values.append(assignee_id)

    if status is not None:
        conditions.append("status = %s")
        values.append(status)

    query = """
        SELECT
            id,
            title,
            description,
            status,
            priority,
            assignee_id,
            due_date,
            created_at,
            updated_at
        FROM tasks
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            rows = cursor.fetchall()

    return [_task_from_row(row) for row in rows]


def update_task(
    task_id,
    title=None,
    description=None,
    status=None,
    priority=None,
    assignee_id=None,
    due_date=None,
):
    updates = []
    values = []

    if title is not None:
        updates.append("title = %s")
        values.append(title)

    if description is not None:
        updates.append("description = %s")
        values.append(description)

    if status is not None:
        updates.append("status = %s")
        values.append(status)

    if priority is not None:
        updates.append("priority = %s")
        values.append(priority)

    if assignee_id is not None:
        updates.append("assignee_id = %s")
        values.append(assignee_id)

    if due_date is not None:
        updates.append("due_date = %s")
        values.append(due_date)

    if not updates:
        return get_task(task_id)

    updates.append("updated_at = CURRENT_TIMESTAMP")

    values.append(task_id)

    query = f"""
        UPDATE tasks
        SET {", ".join(updates)}
        WHERE id = %s
        RETURNING
            id,
            title,
            description,
            status,
            priority,
            assignee_id,
            due_date,
            created_at,
            updated_at
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            row = cursor.fetchone()

    if row is None:
        return None

    return _task_from_row(row)


def complete_task(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET
                    status = 'completed',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    status,
                    priority,
                    assignee_id,
                    due_date,
                    created_at,
                    updated_at
                """,
                (task_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return _task_from_row(row)


def _task_from_row(row):
    return {
        "id": str(row[0]),
        "title": row[1],
        "description": row[2],
        "status": row[3],
        "priority": row[4],
        "assignee_id": row[5],
        "due_date": row[6].isoformat() if isinstance(row[6], date) else row[6],
        "created_at": row[7].isoformat() if row[7] else None,
        "updated_at": row[8].isoformat() if row[8] else None,
    }