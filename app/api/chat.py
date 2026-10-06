from fastapi import APIRouter

from app.agent.service import resume_agent, run_agent
from app.api.schemas import (
    ApprovalRequest,
    ChatRequest,
)
from app.db import (
    create_session,
    save_message,
    session_exists,
)


router = APIRouter()


pending_approvals = {}


@router.post("/chat")
def chat(request: ChatRequest):
    if not session_exists(request.session_id):
        create_session(request.session_id)

    save_message(
        request.session_id,
        "user",
        request.message,
    )

    thread_id = str(request.session_id)

    result = run_agent(
        user_request=request.message,
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

    response = result.get("result", "")

    if not response:
        response = "任务已完成。"

    save_message(
        request.session_id,
        "assistant",
        response,
    )

    return {
        "session_id": request.session_id,
        "status": "completed",
        "response": response,
    }


@router.post("/approval")
def approval(request: ApprovalRequest):
    thread_id = str(request.session_id)

    if thread_id not in pending_approvals:
        return {
            "session_id": request.session_id,
            "status": "error",
            "message": "没有等待审批的请求。",
        }

    result = resume_agent(
        approval=request.approved,
        thread_id=thread_id,
    )

    pending_approvals.pop(thread_id, None)

    response = result.get("result", "")

    if not response:
        if request.approved:
            response = "邮件发送已完成。"
        else:
            response = "邮件发送已取消。"

    save_message(
        request.session_id,
        "assistant",
        response,
    )

    return {
        "session_id": request.session_id,
        "status": "completed",
        "approved": request.approved,
        "response": response,
    }