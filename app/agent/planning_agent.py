import json

from groq import Groq

from app.agent.state import MultiAgentState
from app.tools.employee import search_employee
from app.tools.project import list_projects
from app.tools.task import list_tasks


MODEL = "openai/gpt-oss-120b"

client = Groq()


def planning_agent(state: MultiAgentState):
    print()
    print("========== Planning Agent ==========")
    print()

    user_request = state["user_request"]

    messages = [
        {
            "role": "system",
            "content": """
You are a Planning Agent for an enterprise work assistant.

Your job is to understand the user's request and gather
enterprise information using tools.

Available tools:

- list_projects
- list_tasks
- search_employee

Do not invent enterprise-specific information.

Important error handling rules:

- Tool results may contain an "error" field.
- If a tool returns an error, treat that tool call as failed.
- Do not treat an error result as valid enterprise information.
- Do not invent missing information to compensate for a failed tool.
- If required information cannot be obtained because a tool failed,
  explain that a reliable WorkPlan cannot be produced.

When you have enough information, stop using tools.
The final WorkPlan will be generated in a separate step.

participants must contain employee_id values such as E001.
""",
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_projects",
                "description": "List enterprise projects.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": [
                                "string",
                                "null",
                            ]
                        }
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List enterprise tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": [
                                "string",
                                "null",
                            ]
                        },
                        "project_id": {
                            "type": [
                                "string",
                                "null",
                            ]
                        },
                        "status": {
                            "type": [
                                "string",
                                "null",
                            ]
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_employee",
                "description": "Search an enterprise employee.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "employee_id"
                    ],
                },
            },
        },
    ]

    tool_functions = {
        "list_projects": list_projects,
        "list_tasks": list_tasks,
        "search_employee": search_employee,
    }

    max_iterations = 8
    tool_error = False

    for step in range(max_iterations):
        if tool_error:
            break

        print(
            f"Planning Agent reasoning step "
            f"{step + 1}/{max_iterations}"
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )

        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls

        if not tool_calls:
            print()
            print(
                "Planning Agent finished information gathering."
            )
            break

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in tool_calls
                ],
            }
        )

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(
                tool_call.function.arguments
            )

            print(
                f"Planning Agent requested tool: "
                f"{tool_name}({tool_args})"
            )

            tool = tool_functions[tool_name]
            result = tool(**tool_args)

            print("Tool result:")
            print(result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str,
                    ),
                }
            )

            if isinstance(result, dict) and result.get("error"):
                tool_error = True

                print()
                print(
                    "Planning Agent detected a tool error."
                )

                break

    if tool_error:
        return {
            "work_plan": {},
            "planning_status": "failed",
            "result": (
                "Planning failed because a required "
                "tool returned an error."
            ),
        }

    final_messages = messages + [
        {
            "role": "user",
            "content": """
Based only on the information gathered from the tools,
produce the final WorkPlan.

This is the final planning step.

Do not call any tools.

Return a JSON object only.

Required structure:

{
    "project_id": "...",
    "project_name": "...",
    "meeting_title": "...",
    "participants": ["E001"],
    "reason": "..."
}
""",
        }
    ]

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=final_messages,
        response_format={
            "type": "json_object",
        },
    )

    content = final_response.choices[0].message.content
    work_plan = json.loads(content)

    print()
    print("Planning Agent final response:")
    print(
        json.dumps(
            work_plan,
            ensure_ascii=False,
            indent=4,
        )
    )

    return {
        "work_plan": work_plan,
        "planning_status": "completed",
    }