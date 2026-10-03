from uuid import UUID

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agent.service import run_agent, stream_agent
from app.db import (
    create_session,
    get_messages,
    save_message,
    session_exists,
)

app = FastAPI()


class ChatRequest(BaseModel):
    session_id: UUID
    message: str


@app.get("/")
def root():
    return {"message": "Enterprise AI Work Assistant is running"}


@app.post("/chat")
def chat(request: ChatRequest):
    if not session_exists(request.session_id):
        create_session(request.session_id)

    history = get_messages(request.session_id)

    save_message(
        request.session_id,
        "user",
        request.message,
    )

    messages = history + [
        ("user", request.message)
    ]

    result = run_agent(messages)

    response = result["messages"][-1]

    save_message(
        request.session_id,
        "assistant",
        response.content,
    )

    return {
        "session_id": request.session_id,
        "response": response.content,
    }


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    if not session_exists(request.session_id):
        create_session(request.session_id)

    history = get_messages(request.session_id)

    save_message(
        request.session_id,
        "user",
        request.message,
    )

    messages = history + [
        ("user", request.message)
    ]

    def generate():
        full_response = ""

        for chunk in stream_agent(messages):
            full_response += chunk

            yield f"data: {chunk}\n\n"

        save_message(
            request.session_id,
            "assistant",
            full_response,
        )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )