from groq import Groq
from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState


client = Groq()


def supervisor(state: AgentState):
    """
    Supervisor decides which agent should handle the task next.
    """

    return {
        "user_request": state["user_request"],
    }


def research_agent(state: AgentState):
    """
    Research Agent gathers information needed for the task.

    For this first version, the research result is simulated.
    """

    research_result = """
Remote work policy:
- Employees can work remotely up to 3 days per week.
- Remote work applications must be submitted in advance.
- Employees must remain available during working hours.
""".strip()

    return {
        "user_request": state["user_request"],
        "research_result": research_result,
    }


def writing_agent(state: AgentState):
    """
    Writing Agent creates the final response
    based on the user's request and research result.
    """

    prompt = f"""
You are a workplace writing assistant.

User request:
{state["user_request"]}

Research result:
{state["research_result"]}

Write a clear and professional response based only on
the research result.
Do not invent company-specific policies.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful workplace writing assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    final_answer = response.choices[0].message.content

    return {
        "user_request": state["user_request"],
        "research_result": state["research_result"],
        "final_answer": final_answer,
    }


def build_multi_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor)
    graph.add_node("research_agent", research_agent)
    graph.add_node("writing_agent", writing_agent)

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "research_agent")
    graph.add_edge("research_agent", "writing_agent")
    graph.add_edge("writing_agent", END)

    return graph.compile()