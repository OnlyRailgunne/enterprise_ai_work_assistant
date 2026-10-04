from app.db import get_connection
from app.event_service import (
    create_event as service_create_event,
    get_event as service_get_event,
    list_events as service_list_events,
    cancel_event as service_cancel_event,
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


def create_event(
    title,
    start_time,
    end_time,
    description=None,
    location=None,
    employee_id=None,
):
    organizer_id = None

    if employee_id is not None:
        organizer_id = _get_employee_db_id(employee_id)

        if organizer_id is None:
            return {"error": "Employee not found"}

    return service_create_event(
        title=title,
        start_time=start_time,
        end_time=end_time,
        description=description,
        location=location,
        organizer_id=organizer_id,
    )


def get_event(event_id):
    event = service_get_event(event_id)

    if event is None:
        return {"error": "Event not found"}

    return event


def list_events(employee_id=None):
    organizer_id = None

    if employee_id is not None:
        organizer_id = _get_employee_db_id(employee_id)

        if organizer_id is None:
            return {"error": "Employee not found"}

    return service_list_events(
        organizer_id=organizer_id,
    )


def cancel_event(event_id):
    event = service_cancel_event(event_id)

    if event is None:
        return {"error": "Event not found"}

    return event