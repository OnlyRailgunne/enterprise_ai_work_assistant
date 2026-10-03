
import json

from dotenv import load_dotenv
from groq import Groq
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState
from app.agent.tool_schemas import tool_schemas
from app.tools import TOOLS

load_dotenv()

client = Groq()
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are an enterprise AI assistant.

For questions about company policies, rules, procedures,
internal documents, or other company-specific information:

1. Use the enterprise knowledge tool when relevant.
2. Treat the knowledge tool results as the source of truth.
3. Only state facts that are supported by the retrieved results.
4. Do not add, assume, or invent company-specific information.
5. If the retrieved information is insufficient to answer the question,
   explicitly say that the available knowledge does not contain enough
   information to answer the question.
6. Clearly distinguish between information found in company documents
   and general knowledge.
""".strip()


def agent_node(state: AgentState):
    messages = state["messages"]

    groq_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for message in messages:
        if message.type == "human":
            groq_messages.append({
                "role": "user",
                "content": message.content,
            })

        elif message.type == "ai":
            message_data = {
                "role": "assistant",
                "content": message.content or "",
            }

            if message.tool_calls:
                tool_calls = []

                for tool_call in message.tool_calls:
                    tool_calls.append({
                        "id": tool_call["id"],
                        "type": "function",
                        "function": {
                            "name": tool_call["name"],
                            "arguments": json.dumps(
                                tool_call["args"]
                            ),
                        },
                    })

                message_data["tool_calls"] = tool_calls

            groq_messages.append(message_data)

        elif message.type == "tool":
            groq_messages.append({
                "role": "tool",
                "tool_call_id": message.tool_call_id,
                "content": message.content,
            })

    response = client.chat.completions.create(
        model=MODEL,
        messages=groq_messages,
        tools=tool_schemas,
        tool_choice="auto",
    )

    message = response.choices[0].message

    tool_calls = []

    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_calls.append({
                "name": tool_call.function.name,
                "args": json.loads(
                    tool_call.function.arguments
                ),
                "id": tool_call.id,
            })

    ai_message = AIMessage(
        content=message.content or "",
        tool_calls=tool_calls,
    )

    return {
        "messages": [ai_message]
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
                content=json.dumps(
                    result,
                    ensure_ascii=False,
                ),
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
