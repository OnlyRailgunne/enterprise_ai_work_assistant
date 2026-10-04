
from langgraph.types import Command

from app.agent.graph import graph


def run_agent(messages, thread_id="default"):
    result = graph.invoke(
        {"messages": messages},
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    return result


def resume_agent(approval, thread_id="default"):
    result = graph.invoke(
        Command(resume=approval),
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    return result
