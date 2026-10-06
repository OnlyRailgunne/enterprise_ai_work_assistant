from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]


class MultiAgentState(TypedDict):
    user_request: str

    work_plan: dict
    planning_status: str

    email_draft: dict
    email_draft_id: str
    email_status: str

    next_agent: str

    result: str