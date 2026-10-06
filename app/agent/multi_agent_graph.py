from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.agent.communication_agent import communication_agent
from app.agent.coordinator import (
    coordinator_agent,
    route_from_coordinator,
)
from app.agent.email_agent import (
    create_email_agent,
    send_email_agent,
)
from app.agent.planning_agent import planning_agent
from app.agent.state import MultiAgentState


def build_multi_agent_graph():
    builder = StateGraph(MultiAgentState)

    builder.add_node(
        "coordinator",
        coordinator_agent,
    )

    builder.add_node(
        "planning",
        planning_agent,
    )

    builder.add_node(
        "communication",
        communication_agent,
    )

    builder.add_node(
        "create_email",
        create_email_agent,
    )

    builder.add_node(
        "send_email",
        send_email_agent,
    )

    builder.add_edge(
        START,
        "coordinator",
    )

    builder.add_conditional_edges(
        "coordinator",
        route_from_coordinator,
        {
            "planning": "planning",
            "communication": "communication",
            "create_email": "create_email",
            "send_email": "send_email",
            END: END,
        },
    )

    builder.add_edge(
        "planning",
        "coordinator",
    )

    builder.add_edge(
        "communication",
        "coordinator",
    )

    builder.add_edge(
        "create_email",
        "coordinator",
    )

    builder.add_edge(
        "send_email",
        "coordinator",
    )

    checkpointer = MemorySaver()

    return builder.compile(
        checkpointer=checkpointer,
    )


multi_agent_graph = build_multi_agent_graph()