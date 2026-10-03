import os

import psycopg2


def search_employee(employee_id):
    database_url = os.getenv("DATABASE_URL")

    connection = psycopg2.connect(database_url)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT employee_id, name, department, position
        FROM employees
        WHERE employee_id = %s
        """,
        (employee_id,),
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return {
            "error": "Employee not found"
        }

    return {
        "employee_id": row[0],
        "name": row[1],
        "department": row[2],
        "position": row[3],
    }