import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import ToolMessage

from app.agent.state import AgentState
from app.tools import TOOLS

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)

tools = [
    {
        "name": "search_employee",
        "description": "Search for an employee by employee ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "The employee ID, such as E001.",
                },
            },
            "required": ["employee_id"],
        },
    }
]


def agent_node(state: AgentState):
    messages = state["messages"]

    response = llm.bind_tools(tools).invoke(messages)

    return {
        "messages": [response]
    }


def tool_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        arguments = tool_call["args"]

        tool = TOOLS[tool_name]

        result = tool(**arguments)

        tool_messages.append(
            ToolMessage(
                content=json.dumps(result, ensure_ascii=False),
                tool_call_id=tool_call["id"],
            )
        )

    return {
        "messages": tool_messages
    }


def route_after_agent(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool"

    return END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node(
        "agent",
        agent_node,
    )

    graph.add_node(
        "tool",
        tool_node,
    )

    graph.add_edge(
        START,
        "agent",
    )

    graph.add_conditional_edges(
        "agent",
        route_after_agent,
    )

    graph.add_edge(
        "tool",
        "agent",
    )

    return graph.compile()