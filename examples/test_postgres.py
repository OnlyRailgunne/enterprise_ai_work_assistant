import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


database_url = os.getenv("DATABASE_URL")


with psycopg.connect(database_url) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")

        result = cursor.fetchone()

        print("PostgreSQL connection successful")
        print("Result:", result)