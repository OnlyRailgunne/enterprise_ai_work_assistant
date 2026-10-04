import uuid

from app.db import get_connection


def create_email_draft(
    recipient_id,
    subject,
    body,
):
    draft_id = uuid.uuid4()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO email_drafts (
                    id,
                    recipient_id,
                    subject,
                    body
                )
                VALUES (%s, %s, %s, %s)
                RETURNING
                    id,
                    recipient_id,
                    subject,
                    body,
                    status,
                    created_at,
                    updated_at
                """,
                (
                    draft_id,
                    recipient_id,
                    subject,
                    body,
                ),
            )
            row = cursor.fetchone()

    return _email_draft_from_row(row)


def get_email_draft(draft_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    recipient_id,
                    subject,
                    body,
                    status,
                    created_at,
                    updated_at
                FROM email_drafts
                WHERE id = %s
                """,
                (draft_id,),
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return _email_draft_from_row(row)


def list_email_drafts(
    recipient_id=None,
    status=None,
):
    query = """
        SELECT
            id,
            recipient_id,
            subject,
            body,
            status,
            created_at,
            updated_at
        FROM email_drafts
    """

    conditions = []
    values = []

    if recipient_id is not None:
        conditions.append("recipient_id = %s")
        values.append(recipient_id)

    if status is not None:
        conditions.append("status = %s")
        values.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            rows = cursor.fetchall()

    return [_email_draft_from_row(row) for row in rows]


def update_email_draft(
    draft_id,
    subject=None,
    body=None,
    status=None,
):
    updates = []
    values = []

    if subject is not None:
        updates.append("subject = %s")
        values.append(subject)

    if body is not None:
        updates.append("body = %s")
        values.append(body)

    if status is not None:
        updates.append("status = %s")
        values.append(status)

    if not updates:
        return get_email_draft(draft_id)

    updates.append("updated_at = CURRENT_TIMESTAMP")

    values.append(draft_id)

    query = f"""
        UPDATE email_drafts
        SET {", ".join(updates)}
        WHERE id = %s
        RETURNING
            id,
            recipient_id,
            subject,
            body,
            status,
            created_at,
            updated_at
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            row = cursor.fetchone()

    if row is None:
        return None

    return _email_draft_from_row(row)


def _email_draft_from_row(row):
    return {
        "id": str(row[0]),
        "recipient_id": row[1],
        "subject": row[2],
        "body": row[3],
        "status": row[4],
        "created_at": row[5].isoformat() if row[5] else None,
        "updated_at": row[6].isoformat() if row[6] else None,
    }


def send_email_draft(draft_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE email_drafts
                SET
                    status = 'sent',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND status = 'approved'
                RETURNING
                    id,
                    recipient_id,
                    subject,
                    body,
                    status,
                    created_at,
                    updated_at
                """,
                (draft_id,),
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return _email_draft_from_row(row)


def approve_email_draft(draft_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE email_drafts
                SET
                    status = 'approved',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND status = 'draft'
                RETURNING
                    id,
                    recipient_id,
                    subject,
                    body,
                    status,
                    created_at,
                    updated_at
                """,
                (draft_id,),
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return _email_draft_from_row(row)