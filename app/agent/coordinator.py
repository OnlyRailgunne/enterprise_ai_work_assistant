from langgraph.graph import END

from app.agent.state import MultiAgentState


def coordinator_agent(state: MultiAgentState):
    if state.get("planning_status") == "failed":
        next_agent = "end"

    elif not state.get("work_plan"):
        next_agent = "planning"

    elif not state.get("email_draft"):
        next_agent = "communication"

    elif not state.get("email_draft_id"):
        next_agent = "create_email"

    elif not state.get("email_status"):
        next_agent = "send_email"

    elif state.get("email_status") in {"cancelled", "sent"}:
        next_agent = "end"

    else:
        next_agent = "end"

    print(f"Coordinator decided: {next_agent}")

    return {
        "next_agent": next_agent,
    }


def route_from_coordinator(state: MultiAgentState):
    next_agent = state.get("next_agent")

    if next_agent == "planning":
        return "planning"

    if next_agent == "communication":
        return "communication"

    if next_agent == "create_email":
        return "create_email"

    if next_agent == "send_email":
        return "send_email"

    return END