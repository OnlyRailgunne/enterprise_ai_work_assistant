import uuid

from app.db import session_exists, create_session


session_id = uuid.uuid4()

print("Before:", session_exists(session_id))

create_session(session_id)

print("After:", session_exists(session_id))