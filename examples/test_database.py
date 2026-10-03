import uuid

from app.db import create_session, save_message


session_id = uuid.uuid4()

create_session(session_id)

save_message(
    session_id,
    "user",
    "Hello from database test",
)

print("Session ID:", session_id)
print("Message saved successfully")