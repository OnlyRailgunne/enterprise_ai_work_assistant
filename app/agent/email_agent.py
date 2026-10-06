
import json

from langgraph.types import interrupt

from app.agent.state import MultiAgentState
from app.mcp.email_client import send_email_via_mcp
from app.tools.email import approve_email_draft, create_email_draft


def create_email_agent(state: MultiAgentState):
    print()
    print("========== Create Email Draft ==========")

    email_draft = state["email_draft"]
    recipients = email_draft["recipients"]

    if not recipients:
        return {
            "email_status": "cancelled",
            "result": "No email recipients found.",
        }

    recipient = recipients[0]

    result = create_email_draft(
        employee_id=recipient,
        subject=email_draft["subject"],
        body=email_draft["content"],
    )

    if "error" in result:
        print(
            f"Failed to create email draft: "
            f"{result['error']}"
        )

        return {
            "email_status": "cancelled",
            "result": result["error"],
        }

    draft_id = str(result["id"])

    print(
        f"Created email draft: {draft_id}"
    )

    return {
        "email_draft_id": draft_id
    }


def send_email_agent(state: MultiAgentState):
    print()
    print("========== Email Approval ==========")

    draft_id = state["email_draft_id"]
    email_draft = state["email_draft"]

    approval = interrupt(
        {
            "type": "email_approval",
            "message": "是否发送这封邮件？",
            "draft_id": draft_id,
            "subject": email_draft["subject"],
            "recipients": email_draft["recipients"],
            "content": email_draft["content"],
        }
    )

    if not approval:
        print(
            "Email sending rejected by human."
        )

        return {
            "email_status": "cancelled",
            "result": "Email sending cancelled.",
        }

    print(
        "Email approved. "
        "Approving email draft in database..."
    )

    approved_draft = approve_email_draft(
        draft_id
    )

    if "error" in approved_draft:
        print(
            "Failed to approve email draft:"
        )
        print(
            approved_draft["error"]
        )

        return {
            "email_status": "cancelled",
            "result": (
                "Email approval failed: "
                + approved_draft["error"]
            ),
        }

    print(
        "Email draft approved in database."
    )

    print(
        "Sending through MCP..."
    )

    mcp_result = send_email_via_mcp(
        draft_id
    )

    print("MCP result:")
    print(mcp_result)

    if getattr(
        mcp_result,
        "is_error",
        False,
    ):
        return {
            "email_status": "cancelled",
            "result": "Email sending failed.",
        }

    result_text = ""

    if getattr(
        mcp_result,
        "content",
        None,
    ):
        first_content = mcp_result.content[0]

        if hasattr(
            first_content,
            "text",
        ):
            result_text = first_content.text

    try:
        result_data = json.loads(
            result_text
        )
    except json.JSONDecodeError:
        result_data = {}

    if not result_data.get("success"):
        return {
            "email_status": "cancelled",
            "result": (
                result_data.get(
                    "message",
                    "Email sending failed.",
                )
            ),
        }

    return {
        "email_status": "sent",
        "result": "Email sent successfully.",
    }
