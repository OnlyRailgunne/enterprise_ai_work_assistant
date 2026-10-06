from app.db import get_connection


def _project_from_row(row):
    return {
        "id": row[0],
        "project_id": row[1],
        "name": row[2],
        "description": row[3],
        "status": row[4],
        "created_at": row[5].isoformat(),
        "updated_at": row[6].isoformat(),
    }


def create_project(
    project_id,
    name,
    description=None,
    status="active",
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO projects (
                    project_id,
                    name,
                    description,
                    status
                )
                VALUES (%s, %s, %s, %s)
                RETURNING
                    id,
                    project_id,
                    name,
                    description,
                    status,
                    created_at,
                    updated_at
                """,
                (
                    project_id,
                    name,
                    description,
                    status,
                ),
            )

            row = cursor.fetchone()

    return _project_from_row(row)


def get_project(project_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    project_id,
                    name,
                    description,
                    status,
                    created_at,
                    updated_at
                FROM projects
                WHERE project_id = %s
                """,
                (project_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return _project_from_row(row)


def list_projects(status=None):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            if status is None:
                cursor.execute(
                    """
                    SELECT
                        id,
                        project_id,
                        name,
                        description,
                        status,
                        created_at,
                        updated_at
                    FROM projects
                    ORDER BY created_at DESC
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        id,
                        project_id,
                        name,
                        description,
                        status,
                        created_at,
                        updated_at
                    FROM projects
                    WHERE status = %s
                    ORDER BY created_at DESC
                    """,
                    (status,),
                )

            rows = cursor.fetchall()

    return [_project_from_row(row) for row in rows]


def update_project(
    project_id,
    name=None,
    description=None,
    status=None,
):
    current_project = get_project(project_id)

    if current_project is None:
        return None

    if name is None:
        name = current_project["name"]

    if description is None:
        description = current_project["description"]

    if status is None:
        status = current_project["status"]

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE projects
                SET
                    name = %s,
                    description = %s,
                    status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE project_id = %s
                RETURNING
                    id,
                    project_id,
                    name,
                    description,
                    status,
                    created_at,
                    updated_at
                """,
                (
                    name,
                    description,
                    status,
                    project_id,
                ),
            )

            row = cursor.fetchone()

    return _project_from_row(row)