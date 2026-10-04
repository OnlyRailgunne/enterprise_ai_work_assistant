import json

from groq import Groq
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from app.agent.state import AgentState
from app.agent.tool_schemas import tool_schemas
from app.tools import TOOLS


MODEL = "openai/gpt-oss-120b"

client = Groq()


SYSTEM_PROMPT = """
You are an enterprise AI work assistant.

You can use tools to help users with employees, enterprise knowledge,
tasks, calendar events, and email.

For enterprise-specific policies, procedures, or internal knowledge,
use the enterprise knowledge tool when relevant.

Do not invent company-specific information.

When a tool provides information, use that information as the factual
source for your answer.

For email operations:
- Create an email draft when the user asks you to write an email.
- Do not claim an email was sent unless the send_email tool succeeds.
- Sending an email requires the email draft to be approved first.
"""


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
            groq_messages.append(
                {
                    "role": "user",
                    "content": message.content,
                }
            )

        elif message.type == "ai":
            message_data = {
                "role": "assistant",
                "content": message.content or "",
            }

            if message.tool_calls:
                message_data["tool_calls"] = [
                    {
                        "id": tool_call["id"],
                        "type": "function",
                        "function": {
                            "name": tool_call["name"],
                            "arguments": json.dumps(
                                tool_call["args"],
                                ensure_ascii=False,
                            ),
                        },
                    }
                    for tool_call in message.tool_calls
                ]

            groq_messages.append(message_data)

        elif message.type == "tool":
            groq_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": message.tool_call_id,
                    "content": message.content,
                }
            )

    response = client.chat.completions.create(
        model=MODEL,
        messages=groq_messages,
        tools=tool_schemas,
    )

    choice = response.choices[0]
    assistant_message = choice.message

    tool_calls = []

    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            tool_calls.append(
                {
                    "name": tool_call.function.name,
                    "args": json.loads(
                        tool_call.function.arguments
                    ),
                    "id": tool_call.id,
                    "type": "tool_call",
                }
            )

    return {
        "messages": [
            AIMessage(
                content=assistant_message.content or "",
                tool_calls=tool_calls,
            )
        ]
    }


def tool_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Email sending requires human approval.
        if tool_name == "send_email":
            interrupt(
                {
                    "type": "email_approval",
                    "message": "是否发送这封邮件？",
                    "draft_id": tool_args["draft_id"],
                }
            )

        tool = TOOLS[tool_name]
        result = tool(**tool_args)

        tool_messages.append(
            ToolMessage(
                content=json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str,
                ),
                tool_call_id=tool_call["id"],
            )
        )

    return {
        "messages": tool_messages,
    }


def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool"

    return END


builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tool", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tool": "tool",
        END: END,
    },
)

builder.add_edge("tool", "agent")


checkpointer = MemorySaver()

graph = builder.compile(
    checkpointer=checkpointer,
)