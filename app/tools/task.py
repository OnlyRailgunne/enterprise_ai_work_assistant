from app.db import get_connection
from app.task_service import (
    create_task as service_create_task,
    get_task as service_get_task,
    list_tasks as service_list_tasks,
    update_task as service_update_task,
    complete_task as service_complete_task,
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


def create_task(
    title,
    description=None,
    priority="medium",
    employee_id=None,
    due_date=None,
):
    assignee_id = None

    if employee_id is not None:
        assignee_id = _get_employee_db_id(employee_id)

        if assignee_id is None:
            return {
                "error": "Employee not found",
            }

    return service_create_task(
        title=title,
        description=description,
        priority=priority,
        assignee_id=assignee_id,
        due_date=due_date,
    )


def get_task(task_id):
    task = service_get_task(task_id)

    if task is None:
        return {
            "error": "Task not found",
        }

    return task


def list_tasks(
    employee_id=None,
    status=None,
):
    assignee_id = None

    if employee_id is not None:
        assignee_id = _get_employee_db_id(employee_id)

        if assignee_id is None:
            return {
                "error": "Employee not found",
            }

    return service_list_tasks(
        assignee_id=assignee_id,
        status=status,
    )


def update_task(
    task_id,
    title=None,
    description=None,
    status=None,
    priority=None,
    employee_id=None,
    due_date=None,
):
    assignee_id = None

    if employee_id is not None:
        assignee_id = _get_employee_db_id(employee_id)

        if assignee_id is None:
            return {
                "error": "Employee not found",
            }

    task = service_update_task(
        task_id=task_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        due_date=due_date,
    )

    if task is None:
        return {
            "error": "Task not found",
        }

    return task


def complete_task(task_id):
    task = service_complete_task(task_id)

    if task is None:
        return {
            "error": "Task not found",
        }

    return task