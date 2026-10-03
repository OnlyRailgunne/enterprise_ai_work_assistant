import os
import uuid

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def session_exists(session_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM sessions
                WHERE id = %s
                """,
                (session_id,),
            )

            return cursor.fetchone() is not None


def create_session(session_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sessions (id)
                VALUES (%s)
                """,
                (session_id,),
            )


def save_message(session_id, role, content):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (
                    id,
                    session_id,
                    role,
                    content
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    uuid.uuid4(),
                    session_id,
                    role,
                    content,
                ),
            )


def get_messages(session_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = %s
                ORDER BY created_at ASC
                """,
                (session_id,),
            )

            return cursor.fetchall()


def save_document(filename, content):
    document_id = uuid.uuid4()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    id,
                    filename,
                    content
                )
                VALUES (%s, %s, %s)
                """,
                (
                    document_id,
                    filename,
                    content,
                ),
            )

    return document_id


def save_chunk(document_id, content, embedding):
    chunk_id = uuid.uuid4()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO chunks (
                    id,
                    document_id,
                    content,
                    embedding
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    chunk_id,
                    document_id,
                    content,
                    embedding.tolist(),
                ),
            )

    return chunk_id


def search_chunks(query_embedding, limit=3):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    documents.filename,
                    chunks.content,
                    chunks.embedding <=> %s::vector AS distance
                FROM chunks
                JOIN documents
                    ON chunks.document_id = documents.id
                ORDER BY distance ASC
                LIMIT %s
                """,
                (
                    query_embedding.tolist(),
                    limit,
                ),
            )

            return cursor.fetchall()