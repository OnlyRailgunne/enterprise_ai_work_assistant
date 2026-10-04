from app.db import get_connection
from app.email_service import (
    create_email_draft as service_create_email_draft,
    get_email_draft as service_get_email_draft,
    list_email_drafts as service_list_email_drafts,
    update_email_draft as service_update_email_draft,
    send_email_draft as service_send_email_draft,
    approve_email_draft as service_approve_email_draft,
)


def _get_employee_db_id(employee_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM employees
                WHERE employee_id = %s
                """,
                (employee_id,),
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return row[0]


def create_email_draft(
    employee_id,
    subject,
    body,
):
    recipient_id = _get_employee_db_id(employee_id)

    if recipient_id is None:
        return {"error": "Employee not found"}

    return service_create_email_draft(
        recipient_id=recipient_id,
        subject=subject,
        body=body,
    )


def get_email_draft(draft_id):
    draft = service_get_email_draft(draft_id)

    if draft is None:
        return {"error": "Email draft not found"}

    return draft


def list_email_drafts(
    employee_id=None,
    status=None,
):
    recipient_id = None

    if employee_id is not None:
        recipient_id = _get_employee_db_id(employee_id)

        if recipient_id is None:
            return {"error": "Employee not found"}

    return service_list_email_drafts(
        recipient_id=recipient_id,
        status=status,
    )


def update_email_draft(
    draft_id,
    subject=None,
    body=None,
    status=None,
):
    draft = service_update_email_draft(
        draft_id=draft_id,
        subject=subject,
        body=body,
        status=status,
    )

    if draft is None:
        return {"error": "Email draft not found"}

    return draft


def send_email(draft_id):
    draft = service_send_email_draft(draft_id)

    if draft is None:
        return {
            "error": (
                "Email draft not found or "
                "the draft has not been approved."
            )
        }

    return draft


def approve_email_draft(draft_id):
    draft = service_approve_email_draft(draft_id)

    if draft is None:
        return {
            "error": (
                "Email draft not found or "
                "the draft cannot be approved."
            )
        }

    return draft