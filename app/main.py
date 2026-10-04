from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.service import resume_agent, run_agent
from app.db import (
    create_session,
    get_messages,
    save_message,
    session_exists,
)


app = FastAPI()


pending_approvals = {}


class ChatRequest(BaseModel):
    session_id: UUID
    message: str


class ApprovalRequest(BaseModel):
    session_id: UUID
    approved: bool


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Work Assistant is running"
    }


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

    thread_id = str(request.session_id)

    result = run_agent(
        messages,
        thread_id=thread_id,
    )

    if "__interrupt__" in result:
        interrupt_info = result["__interrupt__"][0]
        approval_data = interrupt_info.value

        pending_approvals[thread_id] = approval_data

        return {
            "session_id": request.session_id,
            "status": "approval_required",
            "approval": {
                "type": approval_data["type"],
                "message": approval_data["message"],
            },
        }

    response = result["messages"][-1]

    save_message(
        request.session_id,
        "assistant",
        response.content,
    )

    return {
        "session_id": request.session_id,
        "status": "completed",
        "response": response.content,
    }


@app.post("/approval")
def approval(request: ApprovalRequest):
    thread_id = str(request.session_id)

    if thread_id not in pending_approvals:
        return {
            "session_id": request.session_id,
            "status": "error",
            "message": "没有等待审批的请求。",
        }

    result = resume_agent(
        request.approved,
        thread_id=thread_id,
    )

    pending_approvals.pop(thread_id, None)

    if request.approved:
        response = result["messages"][-1]

        save_message(
            request.session_id,
            "assistant",
            response.content,
        )

        return {
            "session_id": request.session_id,
            "status": "completed",
            "approved": True,
            "response": response.content,
        }

    return {
        "session_id": request.session_id,
        "status": "completed",
        "approved": False,
        "response": "邮件发送已取消。",
    }