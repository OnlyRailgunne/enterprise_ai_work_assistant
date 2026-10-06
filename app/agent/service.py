from langgraph.types import Command

from app.agent.multi_agent_graph import multi_agent_graph


def run_agent(
    user_request: str,
    thread_id: str = "default",
):
    initial_state = {
        "user_request": user_request,
        "work_plan": {},
        "planning_status": "",
        "email_draft": {},
        "email_draft_id": "",
        "email_status": "",
        "next_agent": "",
        "result": "",
    }

    return multi_agent_graph.invoke(
        initial_state,
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )


def resume_agent(
    approval: bool,
    thread_id: str = "default",
):
    return multi_agent_graph.invoke(
        Command(resume=approval),
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )